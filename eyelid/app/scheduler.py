from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from .models import Timelapse
from . import appbuilder
import cv2
import os

HOST_URL = appbuilder.app.config['HOST_URL']

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': ProcessPoolExecutor(4)
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
scheduler.start()

def schedule_recording(timelapse):
    scheduler.add_job(
        capture_frame,
        trigger='interval',
        max_instances=999999,
        misfire_grace_time=None,
        start_date=timelapse.start_date,
        end_date=timelapse.end_date,
        seconds=timelapse.frequency,
        args=(timelapse.id, timelapse.url, timelapse.folder_name),
    )
    scheduler.add_job(
        render_timelapse,
        trigger='date',
        misfire_grace_time=None,
        run_date=timelapse.end_date,
        args=(timelapse.id, timelapse.folder_name, timelapse.framerate),
    )
    session = appbuilder.get_session()
    timelapse.status = 'queued'
    session.add(timelapse)
    session.commit()

def capture_frame(id, url, folder):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    image_path = './timelapses/{}/{}.jpg'.format(folder, timestamp)
    capture = cv2.VideoCapture(url)
    status, frame = capture.read()
    cv2.imwrite(image_path, frame)
    session = appbuilder.get_session()
    timelapse = session.query(Timelapse).get(id)
    if timelapse.status == 'queued':
        timelapse.status = 'recording'
    timelapse.progress += 1
    timelapse.preview = '{}/preview/{}/{}.jpg'.format(HOST_URL, folder, timestamp)
    session.add(timelapse)
    session.commit()


def render_timelapse(id, folder, framerate):
    session = appbuilder.get_session()
    timelapse = session.query(Timelapse).get(id)
    timelapse.status = 'rendering'
    session.add(timelapse)
    session.commit()
    path = './timelapses/' + folder
    images = sorted(list(os.listdir(path)))
    frame = cv2.imread(os.path.join(path, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(path + '.mp4', fourcc, framerate, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(path, image)))
    video.release()
    timelapse.status = 'done'
    timelapse.video = HOST_URL + '/video/' + folder + '.mp4'
    session.add(timelapse)
    session.commit()

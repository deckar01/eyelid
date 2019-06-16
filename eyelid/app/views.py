from flask import render_template, send_file
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import BaseView, ModelView, ModelRestApi, expose
from flask_appbuilder.api import ModelRestApi
import os

from . import appbuilder, db
from .models import Timelapse
from .scheduler import schedule_recording

class TimelapseApi(ModelRestApi):
    datamodel = SQLAInterface(Timelapse)

appbuilder.add_api(TimelapseApi)


class TimelapseView(ModelView):
    datamodel = SQLAInterface(Timelapse)


appbuilder.add_view(
    TimelapseView,
    "Timelapse View",
    icon="fa-folder-open-o",
    category="Timelapses",
    category_icon='fa-envelope'
)

class TimelapsesApi(ModelRestApi):
    resource_name = 'timelapses'
    datamodel = SQLAInterface(Timelapse)
    order_columns = ('id',)
    base_order = ('id', 'desc')
    list_columns = ('name', 'url', 'start_date', 'end_date', 'frames', 'frequency', 'status', 'progress', 'video', 'preview')
    
    def post_add(self, item):
        os.mkdir('./timelapses/' + item.folder_name)
        schedule_recording(item)


appbuilder.add_api(TimelapsesApi)

class VideoDownload(BaseView):
    route_base = "/video"

    @expose('/<string:name>')
    def serve_video(self, name):
        return send_file('../timelapses/' + name, as_attachment=True)


appbuilder.add_view_no_menu(VideoDownload())

class Preview(BaseView):
    route_base = "/preview"

    @expose('/<string:name>/<string:image>')
    def serve_preview(self, name, image):
        return send_file('../timelapses/{}/{}'.format(name, image))


appbuilder.add_view_no_menu(Preview())

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()

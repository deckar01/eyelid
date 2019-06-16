import os
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_appbuilder.models.decorators import renders
from slugify import slugify

class Timelapse(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    url = Column(String(150), nullable=False)
    start_date = Column(String(150), nullable=False)
    end_date = Column(String(150), nullable=False)
    frames = Column(Integer(), nullable=False)
    frequency = Column(Float(), nullable=False)
    framerate = Column(Integer(), nullable=False)
    progress = Column(Integer(), nullable=False, default=0)
    preview = Column(String(150), nullable=True, default=None)
    video = Column(String(150), nullable=True, default=None)
    status = Column(String(150), nullable=False, default='waiting')
    
    @property
    def folder_name(self):
        return slugify(self.name)

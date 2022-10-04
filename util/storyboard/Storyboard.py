"""
platform: any
env: any
name: Storyboard.py
storyboard and member objects
"""
from util.storyboard.Text import Text
from util.storyboard.Sprite import Sprite
from util.storyboard.Video import Video
from util.storyboard.Line import LineSegments
import json


class StoryBoard:
    def __init__(self):
        self.texts = []                     # list of Text
        self.sprites = []                   # list of Sprite
        self.lines = []                     # list of Line
        self.videos = []                    # list of video
        self.controllers = []               # list of (scene)controller
        self.note_controllers = []          # list of note controller
        self.templates = []                 # list of template

    def add(self, obj):
        """
        add an object to storyboard
        :param obj:
        :return:
        """
        if isinstance(obj, Text):
            self.texts.append(obj)
        elif isinstance(obj, Sprite):
            self.sprites.append(obj)
        elif isinstance(obj, Video):
            self.videos.append(obj)
        elif isinstance(obj, LineSegments):
            self.lines.append(obj)
        else:
            raise (Exception("Error: Object type not supported."))

    def parse(self):
        """
        Parse object to storyboard string
        :return:
        """
        ret = {}
        if len(self.texts) > 0:
            ret["texts"] = []
            for text in self.texts:
                for state in text.to_storyboard():
                    ret["texts"].append(state)
        if len(self.sprites) > 0:
            ret["sprites"] = []
            for sprite in self.sprites:
                for state in sprite.to_storyboard():
                    ret["sprites"].append(state)
        if len(self.lines) > 0:
            ret["lines"] = []
            for line in self.lines:
                state = line.to_storyboard()
                ret["lines"].append(state)
        if len(self.videos) > 0:
            ret["videos"] = []
            for video in self.videos:
                for state in video.to_storyboard():
                    ret["videos"].append(state)
        if len(self.controllers) > 0:
            ret["controllers"] = [i.to_dict() for i in self.controllers]
        if len(self.note_controllers) > 0:
            ret["note_controllers"] = [i.to_dict() for i in self.note_controllers]
        if len(self.templates) > 0:
            ret["templates"] = [i.to_dict() for i in self.templates]
        return json.dumps(ret)

"""
platform: any
env: any
name: Storyboard.py
storyboard and member objects
"""
from util.storyboard.Text import Text
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
        else:
            raise (Exception("Error: Object type not supported."))

    def parse(self):
        """
        Parse object to storyboard string
        :return:
        """
        ret = {}
        if len(self.texts) > 0:
            ret["texts"] = [i.to_dict() for i in self.texts]
        if len(self.sprites) > 0:
            ret["sprites"] = [i.to_dict() for i in self.sprites]
        if len(self.lines) > 0:
            ret["lines"] = [i.to_dict() for i in self.lines]
        if len(self.videos) > 0:
            ret["videos"] = [i.to_dict() for i in self.videos]
        if len(self.controllers) > 0:
            ret["controllers"] = [i.to_dict() for i in self.controllers]
        if len(self.note_controllers) > 0:
            ret["note_controllers"] = [i.to_dict() for i in self.note_controllers]
        if len(self.templates) > 0:
            ret["templates"] = [i.to_dict() for i in self.templates]
        return json.dumps(ret)

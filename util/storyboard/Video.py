"""
platform: any
env: any
name: Video.py
video object and its state
"""
from util.storyboard.SceneObject import SceneObject, SceneObjectState


class VideoState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.path = ""                          # relative path to video
        self.color = "#FFF"                     # hex string for tint color

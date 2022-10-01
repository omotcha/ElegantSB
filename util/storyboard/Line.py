"""
platform: any
env: any
name: Line.py
line object and its state
"""
from util.storyboard.SceneObject import SceneObject, SceneObjectState


class LineState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.pos = []                           # list of Vertex
        self.width = 0.05
        self.color = "#FFF"                     # hex string

"""
platform: any
env: any
name: Sprite.py
sprite object and its state
"""
from util.storyboard.SceneObject import SceneObject, SceneObjectState


class SpriteState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.path = ""                          # relative path to image
        self.preserve_aspect = True             # whether image aspect ratio is preserved
        self.color = "#FFF"                     # hex string for tint color

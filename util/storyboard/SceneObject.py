"""
platform: any
env: any
name: SceneObject.py
scene object and its state
"""
import json


class SceneObjectState:
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """

        # basic params
        self.time = time  # absolute time
        self.easing = easing  # easing
        self.destroy = False  # destroy

        # placing
        self.x = 0  # stageX coord sys
        self.y = 0  # stageY coord sys
        self.z = 0  # depth coord sys

        # rotating
        self.rot_x = 0  # degrees
        self.rot_y = 0  # degrees
        self.rot_z = 0  # degrees

        # scaling
        self.scale_x = 1  # scale on x-axis
        self.scale_y = 1  # scale on y-axis
        self.scale = 1  # scale on both x and y-axis

        # pivot for rotating/scaling
        self.pivot_x = 0.5  # 0 for left, 1 for right, 0.5 for center
        self.pivot_y = 0.5  # 0 for left, 1 for right, 0.5 for center

        # opacity
        self.opacity = 0  # 0 for invisible, 1 for visible

        # size
        self.width = 200  # for sprites
        self.height = 200  # for sprites

        # layer placing
        # 0 for background | obj | other game elements | ui
        # 1 for background | other game elements | obj | ui
        # 2 for background | other game elements | ui | obj
        self.layer = 0

        # same-layer object priority
        self.order = 0  # higher ordered obj will display more in front

        # stretching
        self.fill_width = False  # if True, width <- stage's width, height <- 10000

    def to_dict(self):
        ret = {
            "time": self.time,
            "easing": self.easing,
            "destroy": self.destroy,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "rot_x": self.rot_x,
            "rot_y": self.rot_y,
            "rot_z": self.rot_z,
            "scale_x": self.scale_x,
            "scale_y": self.scale_y,
            "scale": self.scale,
            "pivot_x": self.pivot_x,
            "pivot_y": self.pivot_y,
            "opacity": self.opacity,
            "width": self.width,
            "height": self.height,
            "layer": self.layer,
            "order": self.order,
            "fill_width": self.fill_width
        }
        return ret


class SceneObject:
    """
    [omo]tcha: SceneObject just looks like an interface, of which the actions are not implemented.
    So do not use it directly until you implement it yourself.
    """
    def __init__(self):
        """
        Create an object.
        self._id is a unique id of an object
        self._states is a dictionary that holds states of all modified properties with respect to time
        self._current_state is the object lifecycle state
        self._hatch_time is when the object is hatched
        """
        self._id = str(id(self))
        self._states = {}
        self._current_state = "egg"
        self._hatch_time = 0

    def hatch(self, at, init=None):
        """
        It should be the first action(or state change) of an object.
        After that, the object's state is "active" and listens for next action
        :param at: when to hatch (absolute time)
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            # you should add an initial scene object state here ↓

            # you should add an initial scene object state here ↑
            self._current_state = "active"
            self._hatch_time = at
            print("A scene object is hatched.")
        else:
            raise(Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
        return self

    def move(self, at, to, duration, animation):
        """
        Change position-related state property of an active object
        :param at: when to move (absolute time)
        :param to: where to move to ((x, y) in stageXY coord sys)
        :param duration: how long to move (time)
        :param animation: how to move (Animation)
        :return:
        """
        if self._current_state == "active":
            # you should add a new scene object state here ↓

            # you should add a new scene object state here ↑
            print("A scene object moves.")
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def rotate(self, at, axis, degree, duration, animation):
        """
        Change rotation-related state property of an active object
        :param at: when to rotate (absolute time)
        :param axis: on which axis to rotate ("x"/"y"/"z" str)
        :param degree: degree to rotate (number)
        :param duration: how long to move (time)
        :param animation: how to move (Animation)
        :return:
        """
        if self._current_state == "active":
            # you should add a new scene object state here ↓

            # you should add a new scene object state here ↑
            print("A scene object rotates.")
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def morph(self, prop, value, at, duration, animation):
        """
        Change one morphology-related state property of an active object
        :param prop: which property to morph (str)
        :param value: new property value (any matched value)
        :param at: when to morph (absolute time)
        :param duration: how long to morph (time)
        :param animation: how to morph (Animation)
        :return:
        """
        if self._current_state == "active":
            # you should add a new scene object state here ↓

            # you should add a new scene object state here ↑
            print("A scene object morphs.")
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def imitate(self, at, target):
        """
        Current object imitates (hard_copy) the latest state of another object
        This is a "higher-level" action of an object, so treat it carefully
        :param at: when to imitate (absolute time)
        :param target: the target object to imitate (SceneObject)
        :return:
        """
        if self._current_state == "active":
            # you should add a new scene object state here ↓

            # you should add a new scene object state here ↑
            print("A scene object imitates.")
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def get_latest_state(self):
        keys = self._states.keys()
        if len(keys) == 0:
            return None
        else:
            return self._states[max(keys)]

    def to_dict(self):
        """
        Parse object to storyboard dictionary, do not use it directly
        :return:
        """
        return

"""
platform: any
env: any
name: SceneObject.py
scene object and its state
"""
from util.storyboard.base import ActionPipe
from copy import deepcopy


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

        # [omo]tcha: here I limit some properties' ability to morph
        self._morphable_props = ["opacity", "layer", "order"]
        self._scalable_props = ["scale", "scale_x", "scale_y"]
        self._settable_props = ["pivot_x", "pivot_y", "destroy"]
        self._movable_props = ["x", "y"]
        self._rotatable_props = ["rot_x", "rot_y", "rot_z"]

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

    def init(self):
        ret = {}
        for prop in self._morphable_props + self._scalable_props + self._settable_props + self._rotatable_props:
            ret[prop] = self.__getattribute__(prop)
        return ret


class SceneObject:
    """
    [omo]tcha: SceneObject just looks like an interface, of which the actions are not fully implemented.
    So do not use it directly unless you implement it yourself.
    """
    def __init__(self):
        """
        Create an object.
        self._id is a unique id of an object
        self._current_state is the object lifecycle state
        self._hatch_time is when the object is hatched
        self._actions is the dictionary of action pipelines
        self._delay is used when imitating
        """
        self._id = str(id(self))
        self._current_state = "egg"
        self._hatch_time = 0
        self._actions = {}
        self._delay = 0

        # [omo]tcha: here I limit some properties' ability to morph
        self._morphable_props = ["opacity", "layer", "order"]
        self._scalable_props = ["scale", "scale_x", "scale_y"]
        self._settable_props = ["pivot_x", "pivot_y", "destroy"]
        self._movable_props = ["x", "y"]
        self._rotatable_props = ["rot_x", "rot_y", "rot_z"]

        # [omo]tcha: the coordinate system type of scene object, default: stage
        # not settable
        self._coord_sys = "stage"

    def hatch(self, at, to=(0, 0), init=None):
        """
        It should be the first action(or state change) of an object.
        After that, the object's state is "active" and listens for next action
        :param at: when to hatch (absolute time)
        :param to: where to hatch ((x, y) in stageXY coord sys)
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
            if init is not None:
                if isinstance(init, dict):
                    for k in init.keys():
                        # [omo]tcha: init can be regarded as the first morph
                        if k not in self._morphable_props + self._rotatable_props \
                                + self._scalable_props + self._settable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    init["x"] = to[0]
                    init["y"] = to[1]
                    for k in init.keys():
                        self._actions[k] = ActionPipe(at, init[k])
                else:
                    raise (Exception("ParameterError: init should be a dictionary."))
            self._current_state = "active"
            self._hatch_time = at
        else:
            raise (Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
        return self

    def move(self, at, to, duration, animation=None):
        """
        Change position-related state property of an active object
        :param at: when to move (absolute time)
        :param to: where to move to ((x, y) in stageXY coord sys)
        :param duration: how long to move (time)
        :param animation: how to move (Animation)
        :return:
        """
        if self._current_state == "active":
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if to[0] is None and to[1] is None:
                raise (Exception("ValueError: Please specify at least one not-None value."))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            if to[0] is not None:
                if "x" not in self._actions.keys():
                    self._actions["x"] = ActionPipe(self._hatch_time, to[0])
                self._actions["x"].add(at, duration=duration, value=to[0], easing=easing)

            if to[1] is not None:
                if "y" not in self._actions.keys():
                    self._actions["y"] = ActionPipe(self._hatch_time, to[1])
                self._actions["y"].add(at, duration=duration, value=to[1], easing=easing)

        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def rotate(self, at, axis, degree, duration, animation=None, pivot=None):
        """
        Change rotation-related state property of an active object
        :param at: when to rotate (absolute time)
        :param axis: on which axis to rotate ("x"/"y"/"z" str)
        :param degree: degree to rotate (number)
        :param duration: how long to move (time)
        :param animation: how to move (Animation)
        :param pivot: pivot of rotation
        :return:
        """
        if self._current_state == "active":
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if axis not in ["x", "y", "z"]:
                raise (Exception("ValueError: Axis should be like 'x'/'y'/'z', but have {}".format(axis)))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            prop = "rot_{}".format(axis)
            if prop not in self._actions.keys():
                self._actions[prop] = ActionPipe(self._hatch_time, degree)
            self._actions[prop].add(at, duration=duration, value=degree, easing=easing)

            if axis == "x" or axis == "y" and pivot is not None:
                prop = "pivot_{}".format(axis)
                if prop not in self._actions.keys():
                    self._actions[prop] = ActionPipe(self._hatch_time, pivot)
                self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)

        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def scale(self, at, axis, value, duration, animation=None, pivot=None):
        """
        Change scaling-related state property of an active object
        :param at: when to scale (absolute time)
        :param axis: on which axis to scale ("x"/"y"/"xy" str)
        :param value: scaling factor
        :param duration: how long to move (time)
        :param animation: how to move (Animation indicating easing)
        :param pivot: pivot: pivot of scaling
        :return:
        """
        if self._current_state == "active":
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if axis not in ["x", "y", "xy"]:
                raise (Exception("ValueError: Axis should be like 'x'/'y'/'xy', but have {}".format(axis)))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            if axis == "xy":
                prop = "scale"
            else:
                prop = "scale_{}".format(axis)
            if prop not in self._actions.keys():
                self._actions[prop] = ActionPipe(self._hatch_time, value)
            self._actions[prop].add(at, duration=duration, value=value, easing=easing)

            if pivot is not None:
                if axis != "x":
                    prop = "pivot_y"
                    if prop not in self._actions.keys():
                        self._actions[prop] = ActionPipe(self._hatch_time, pivot)
                    self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)
                if axis != "y":
                    prop = "pivot_x"
                    if prop not in self._actions.keys():
                        self._actions[prop] = ActionPipe(self._hatch_time, pivot)
                    self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)

        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def morph(self, at, to_morph, duration, animation=None):
        """
        Change one morphology-related state property of an active object
        :param at: when to morph (absolute time)
        :param to_morph: which properties to morph (dictionary of (property to morph, new value))
        :param duration: how long to morph (time)
        :param animation: how to morph (Animation)
        :return:
        """
        if self._current_state == "active":
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))

            easing = animation.easing if animation is not None else "linear"

            if to_morph is not None:
                if isinstance(to_morph, dict):
                    for k in to_morph.keys():
                        if k not in self._morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for morphing.".format(k)))

                    for k in to_morph.keys():
                        if k not in self._actions.keys():
                            self._actions[k] = ActionPipe(self._hatch_time, to_morph[k])
                        self._actions[k].add(at, duration=duration, value=to_morph[k], easing=easing)

                else:
                    raise (Exception("ParameterError: to_morph should be a dictionary."))
            else:
                print("Warning: Nothing to morph.")
                return self
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def mutate(self, at, to_mutate, animation=None):
        """
        Change one property of an active object in a short time period like a pulse.
        This may be conflict with morph() cuz they may write on same action pipe, treat it carefully
        :param at: when to mutate (absolute time)
        :param to_mutate: which properties to mutate (dictionary of (property to mutate, mutate value))
        :param animation: animation: how to mutate (Animation indicating easing and mutate_interval)
        :return:
        """
        if self._current_state == "active":
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))

            easing = animation.easing if animation is not None else "linear"
            mutate_interval = animation.mutate_interval if animation is not None else 0.05

            if to_mutate is not None:
                if isinstance(to_mutate, dict):
                    for k in to_mutate.keys():
                        if k not in self._morphable_props + self._movable_props \
                                + self._scalable_props + self._rotatable_props:
                            raise (Exception("KeyError: Key {} cannot be used for mutating.".format(k)))

                    for k in to_mutate.keys():
                        if k not in self._actions.keys():
                            raise (Exception("LogicError: A property should be declared before doing mutation"))
                        val_retrieve = self._actions[k].get_latest_value(at - mutate_interval)
                        self._actions[k].add(at - mutate_interval,
                                             duration=mutate_interval,
                                             value=to_mutate[k],
                                             easing=easing)
                        self._actions[k].add(at,
                                             duration=mutate_interval,
                                             value=val_retrieve,
                                             easing=easing)

                else:
                    raise (Exception("ParameterError: to_mutate should be a dictionary."))
            else:
                print("Warning: Nothing to mutate.")
                return self
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def imitate(self, at, target):
        """
        Current object follows another object.
        By imitating, the object forgets all previously defined actions and follow the target ones.
        Here "follow" is not logically-true if at is smaller than the hatch time of target.
        In such case, it is like target is "following" this object.
        This is a "higher-level" action of an object, treat it carefully
        :param at: when to imitate (absolute time)
        :param target: the target object to imitate (SceneObject)
        :return:
        """
        if self._current_state == "active":
            # you should add a new scene object state/action here ↓

            # you should add a new scene object state/action here ↑
            print("A scene object imitates.")
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def destroy(self, at):
        """
        Destroy the object
        :param at: time to destroy (absolute time)
        :return:
        """
        if self._current_state == "active":
            if at <= self._hatch_time:
                raise (Exception("ValueError: Cannot destroy an object before it hatches."))
            if "destroy" not in self._actions.keys():
                self._actions["destroy"] = ActionPipe(self._hatch_time, False)
            self._actions["destroy"].add(at, duration=0.01, value=True, easing="linear")
            self._current_state = "destroyed"
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def get_hatch_time(self):
        return self._hatch_time

    def copy_actions(self):
        ret = {}
        for k, v in self._actions.items():
            ret[k] = deepcopy(v)
        return ret

    def to_storyboard(self):
        """
        Parse object to storyboard object, do not use it directly
        :return:
        """
        return

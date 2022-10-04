"""
platform: any
env: any
name: Text.py
text object and its state
"""
from util.storyboard.base import Animation
from util.storyboard.SceneObject import SceneObject, SceneObjectState
from util.storyboard.base import ActionPipe
from copy import deepcopy

# [omo]tcha: here I limit some properties' ability to morph
morphable_props = ["opacity", "layer", "order", "color", "align", "letter_spacing", "font_weight"]
scalable_props = ["scale", "scale_x", "scale_y"]
settable_props = ["pivot_x", "pivot_y", "destroy"]
movable_props = ["x", "y"]
rotatable_props = ["rot_x", "rot_y", "rot_z"]


class TextState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.color = "#FFF"  # hex string
        self.size = 20  # font size, integer
        self.align = "middleCenter"  # upper|middle|lower + Left|Center|Right
        self.letter_spacing = 0  # letter spacing
        self.font_weight = "regular"  # regular|extraLight|bold|extraBold

    def to_dict(self):
        ret = super().to_dict()
        ret["color"] = self.color
        ret["size"] = self.size
        ret["align"] = self.align
        ret["letter_spacing"] = self.letter_spacing
        ret["font_weight"] = self.font_weight
        return ret

    def init(self):
        ret = {}
        for prop in morphable_props + scalable_props + settable_props + rotatable_props:
            ret[prop] = self.__getattribute__(prop)
        return ret


class Text(SceneObject):
    def __init__(self, text_content):
        """

        :param text_content:
        """
        super().__init__()
        self._text = text_content
        self._id = "text_" + self._id

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
                        if k not in morphable_props + rotatable_props + scalable_props + settable_props:
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
                        if k not in morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for morphing.".format(k)))

                    for k in to_morph.keys():
                        if k not in self._actions.keys():
                            self._actions[k] = ActionPipe(self._hatch_time, to_morph[k])
                        self._actions[k].add(at, duration=duration, value=to_morph[k], easing=easing)

                else:
                    raise (Exception("ParameterError: to_morph should be a dictionary."))
            else:
                print("Warning: Nothing to morph")
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
                        if k not in morphable_props + movable_props + scalable_props + rotatable_props:
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
                    raise (Exception("ParameterError: to_morph should be a dictionary."))
            else:
                print("Warning: Nothing to morph")
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
        self._current_state = "active"
        self._hatch_time = at
        if at < 0:
            raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))

        if not isinstance(target, Text):
            raise (Exception("TypeError: Imitation between different species is not supported."))
        self._actions = target.copy_actions()
        self._delay = at - target.get_hatch_time()
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
        Parse pipes to states then to storyboard objects
        :return:
        """
        first = True
        ret = []
        for prop, pipe in self._actions.items():
            pipe = pipe.to_list()
            # [omo]tcha: the first item has text content and its id,
            # while the other items are targeted to the first one
            if first:
                dic_first = {
                    "text": self._text,
                    "id": self._id,
                    "states": [{
                        "time": pipe[0][0]+self._delay,
                        prop: pipe[0][2],
                        "easing": pipe[0][3]
                    }]
                }
                for i in range(1, len(pipe)):
                    dic_first["states"].append({
                        "time": pipe[i][0]+self._delay,
                        prop: pipe[i-1][2],
                        "easing": pipe[i][3]
                    })
                    dic_first["states"].append({
                        "time": pipe[i][1]+self._delay,
                        prop: pipe[i][2],
                        "easing": pipe[i-1][3]
                    })
                ret.append(dic_first)
                first = False
            else:
                dic = {
                    "target_id": self._id,
                    "states": [{
                        "time": pipe[0][0]+self._delay,
                        prop: pipe[0][2],
                        "easing": pipe[0][3]
                    }]
                }
                for i in range(1, len(pipe)):
                    dic["states"].append({
                        "time": pipe[i][0]+self._delay,
                        prop: pipe[i-1][2],
                        "easing": pipe[i][3]
                    })
                    dic["states"].append({
                        "time": pipe[i][1]+self._delay,
                        prop: pipe[i][2],
                        "easing": pipe[i-1][3]
                    })
                ret.append(dic)
        return ret


if __name__ == '__main__':
    inSineAnimation = Animation()
    inSineAnimation.easing = "easeInSine"
    elegantTxt = Text("elegant").hatch(at=10, to=(50, 50), init={"color": "#F00", "opacity": 0, "scale": 1})\
                                .morph(at=11, to_morph={"opacity": 1}, duration=1)\
                                .move(at=11, to=(100, 200), duration=10, animation=inSineAnimation)\
                                .mutate(at=20, to_mutate={"scale": 2}, animation=inSineAnimation)

    anotherTxt = Text("storyboarding").imitate(at=33, target=elegantTxt)
    print(elegantTxt.to_storyboard())
    print(anotherTxt.to_storyboard())

"""
platform: any
env: any
name: Text.py
text object and its state
"""
from util.storyboard.base import Animation
from util.storyboard.SceneObject import SceneObject, SceneObjectState
from bisect import bisect_right
from copy import deepcopy

# [omo]tcha: here I limit some properties' ability to morph
morphable_props = ["size", "opacity", "layer", "order", "color", "align", "letter_spacing", "font_weight"]
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


class Text(SceneObject):
    def __init__(self, text_content):
        """

        :param text_content:
        """
        super().__init__()
        self._text = text_content
        self._id = "text_" + self._id

    def hatch(self, at, init=None):
        """
        It should be the first action(or state change) of an object.
        After that, the object's state is "active" and listens for next action
        :param at: when to hatch (absolute time)
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
            self._states[at] = TextState(time=at, easing="linear")
            if init is not None:
                if isinstance(init, dict):
                    for k in init.keys():
                        # [omo]tcha: init can be regarded as the first morph
                        if k not in morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    for k in init.keys():
                        setattr(self._states[at], k, init[k])
                else:
                    raise (Exception("ParameterError: init should be a dictionary."))
            self._current_state = "active"
            self._hatch_time = at
        else:
            raise (Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
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
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if to[0] is None and to[1] is None:
                raise (Exception("ValueError: Please specify at least one not-None value."))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            # inherit a state with the latest time
            latest_t = self.inherit_latest_state(at=at, easing=easing)

            des_time = at + duration
            if des_time in self._states.keys():
                if to[0] is not None:
                    self._states[des_time].x = to[0]
                if to[1] is not None:
                    self._states[des_time].y = to[1]
            else:
                des_state = deepcopy(self._states[at])
                des_state.time = des_time
                des_state.easing = self._states[latest_t].easing
                if to[0] is not None:
                    des_state.x = to[0]
                if to[1] is not None:
                    des_state.y = to[1]
                self._states[des_time] = des_state
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
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if axis not in ["x", "y", "z"]:
                raise (Exception("ValueError: Axis should be like 'x'/'y'/'z', but have {}".format(axis)))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            # inherit a state with the latest time
            latest_t = self.inherit_latest_state(at=at, easing=easing)

            des_time = at + duration
            if des_time in self._states.keys():
                if axis == "x":
                    self._states[des_time].rot_x = degree
                elif axis == "y":
                    self._states[des_time].rot_y = degree
                else:
                    self._states[des_time].rot_z = degree
            else:
                des_state = deepcopy(self._states[at])
                des_state.time = des_time
                des_state.easing = self._states[latest_t].easing
                if axis == "x":
                    des_state.rot_x = degree
                elif axis == "y":
                    des_state.rot_y = degree
                else:
                    des_state.rot_z = degree
                self._states[des_time] = des_state
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def morph(self, at, to_morph, duration, animation):
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
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))

                    # inherit a state with the latest time
                    latest_t = self.inherit_latest_state(at=at, easing=easing)

                    des_time = at + duration
                    if des_time in self._states.keys():
                        for k in to_morph.keys():
                            setattr(self._states[des_time], k, to_morph[k])
                    else:
                        des_state = deepcopy(self._states[at])
                        des_state.time = des_time
                        des_state.easing = self._states[latest_t].easing
                        for k in to_morph.keys():
                            setattr(des_state, k, to_morph[k])
                        self._states[des_time] = des_state
                else:
                    raise (Exception("ParameterError: to_morph should be a dictionary."))
            else:
                print("Warning: Nothing to morph")
                return self
        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def to_dict(self):
        """
        Parse object to storyboard dictionary
        :return:
        """
        ret = {"text": self._text, "states": []}
        for _, state in self._states.items():
            ret["states"].append(state.to_dict())
        return ret

    def inherit_latest_state(self, at, easing):
        """
        deep copy the latest state to current time
        [omo]tcha: the auto-update of state inheritance is not supported,
        that is to say, if later you add a state with time new_t within (latest_t, at),
        this latest_t and the state at this time would not be updated automatically,
        thus the storyboard may not behave as expected
        :param at: current time (absolute time)
        :param easing: easing at current time
        :return:
        """
        key_list = list(self._states.keys())
        bi = bisect_right(key_list, at)
        if bi:
            latest_t = key_list[bi - 1]
            if latest_t < at:
                at_state = deepcopy(self._states[latest_t])
                at_state.time = at
                at_state.easing = easing
                self._states[at] = at_state
        else:
            raise (Exception("ValueError: Unexpected bisection error for time: {}".format(at)))
        return latest_t


if __name__ == '__main__':
    ani = Animation()
    ani.easing = "easeInBack"
    elegantTxt = Text("elegant").hatch(at=10, init={"color": "#F00"})\
                                .morph(at=11, to_morph={"opacity": 1}, duration=1, animation=ani)\
                                .move(at=11, to=(100, 200), duration=10, animation=ani)
    print(elegantTxt.to_dict())

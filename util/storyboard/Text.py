"""
platform: any
env: any
name: Text.py
text object and its state
"""
from util.storyboard.SceneObject import SceneObject, SceneObjectState


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
        After that, the object's is "active" and listens for next action
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
                        if k not in dir(self._states[at]):
                            raise (Exception("KeyError: Key {} not found in TextState.".format(k)))
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
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
            if to[0] is None and to[1] is None:
                raise (Exception("ValueError: Please specify at least one not-None value."))

            print("A scene object moves.")
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


if __name__ == '__main__':
    elegant = Text("elegant").hatch(at=10, init={"color": "#F00"})
    print(elegant.to_dict())

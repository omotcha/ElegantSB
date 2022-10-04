"""
platform: any
env: any
name: Text.py
text object and its state
"""
from util.storyboard.base import *
from util.storyboard.SceneObject import *
from copy import deepcopy


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

        self._morphable_props += ["color", "align", "letter_spacing", "font_weight"]

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
        for prop in self._morphable_props + self._scalable_props + self._settable_props + self._rotatable_props:
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

        self._morphable_props += ["color", "align", "letter_spacing", "font_weight"]

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

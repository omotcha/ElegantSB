"""
platform: any
env: any
name: Sprite.py
sprite object and its state
"""
from util.storyboard.base import *
from util.storyboard.SceneObject import *
from copy import deepcopy


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

        self._morphable_props += ["color"]
        self._settable_props += ["preserve_aspect"]

    def to_dict(self):
        ret = super().to_dict()
        ret["color"] = self.color
        ret["preserve_aspect"] = self.preserve_aspect
        return ret

    def init(self):
        ret = {}
        for prop in self._morphable_props + self._scalable_props + self._settable_props + self._rotatable_props:
            ret[prop] = self.__getattribute__(prop)
        return ret


class Sprite(SceneObject):
    def __init__(self, path):
        """

        :param path:
        """
        super().__init__()
        self._path = path
        self._id = "sprite_" + self._id

        self._morphable_props += ["color"]
        self._settable_props += ["preserve_aspect"]

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

        if not isinstance(target, Sprite):
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
            # [omo]tcha: the first item has path to sprite and its id,
            # while the other items are targeted to the first one
            if first:
                dic_first = {
                    "path": self._path,
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

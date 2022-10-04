"""
platform: any
env: any
name: Line.py
line object and its state
"""
from util.storyboard.base import ActionPipe, Vertex
from copy import deepcopy


class LineSegmentsState:
    def __init__(self, time, pos):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param pos: list of vertex
        """
        self.time = time
        self.pos = pos if pos is not None else []
        self.width = 0.05
        self.color = "#FFF"                     # hex string
        self.opacity = 0
        self.layer = 0
        self.order = 0
        self.destroy = False

        self._len = len(self.pos)

        self._morphable_props = ["opacity", "color", "width", "layer", "order", "pos"]
        self._settable_props = ["destroy"]

    def to_dict(self):
        ret = {
            "time": self.time,
            "destroy": self.destroy,
            "opacity": self.opacity,
            "color": self.color,
            "width": self.width,
            "layer": self.layer,
            "order": self.order,
            "pos": [{"x": i.x, "y": i.y} for i in self.pos],
        }
        return ret

    def init(self):
        ret = {}
        for prop in self._morphable_props + self._settable_props:
            ret[prop] = self.__getattribute__(prop)
        return ret


class LineSegments:
    def __init__(self):
        """
        Create a line segments object. Line segments object consists of connected line segments
        self._id is a unique id of an object
        self._current_state is the object lifecycle state
        self._hatch_time is when the object is hatched
        self._actions is the dictionary of action pipelines
        self._delay is used when imitating
        self._len is the length of position list, it cannot be modified during the object's lifecycle
        """
        self._id = "lines_" + str(id(self))
        self._current_state = "egg"
        self._hatch_time = 0
        self._actions = {}
        self._delay = 0
        self._len = 0

        self._morphable_props = ["opacity", "color", "width", "layer", "order", "pos"]
        self._settable_props = ["destroy"]

    def hatch(self, at, pos, init=None):
        """
        It should be the first action(or state change) of an object.
        After that, the object's state is "active" and listens for next action
        :param at: when to hatch (absolute time)
        :param pos: the initial positions of vertices (list of Vertex)
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            if at < 0:
                raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
            if not isinstance(pos, list):
                raise (Exception("TypeError: Pos should be list<Vertex>."))
            for v in pos:
                if not isinstance(v, Vertex):
                    raise (Exception("TypeError: Pos should be list<Vertex>."))

            if init is not None:
                if isinstance(init, dict):
                    for k in init.keys():
                        # [omo]tcha: init can be regarded as the first morph
                        if k not in self._morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    self._actions["pos"] = ActionPipe(at, pos)
                    for k in init.keys():
                        self._actions[k] = ActionPipe(at, init[k])
                else:
                    raise (Exception("ParameterError: init should be a dictionary."))
            self._current_state = "active"
            self._hatch_time = at
            self._len = len(pos)
        else:
            raise (Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
        return self

    def move(self, at, shift, duration):
        """
        Change position-related state property of an active object
        :param at: when to move (absolute time)
        :param shift: the shift in xy-axis ((x, y) in stageXY coord sys)
        :param duration: how long to move (time)
        :return:
        """
        if self._current_state == "active":
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if shift[0] is None and shift[1] is None:
                raise (Exception("ValueError: Please specify at least one not-None value."))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))
            if "pos" not in self._actions.keys():
                raise (Exception("LogicError: Line segments should have initial positions."))

            latest_pos = self._actions["pos"].get_latest_value(at)

            new_pos = []

            if shift[0] is None:
                shift[0] = 0
            if shift[1] is None:
                shift[1] = 0

            for i in range(self._len):
                v = Vertex(x=latest_pos[i].x + shift[0], y=latest_pos[i].y + shift[1])
                new_pos.append(v)

            self._actions["pos"].add(at, duration=duration, value=new_pos, easing="linear")

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
                        if k not in self._morphable_props:
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
        self._current_state = "active"
        self._hatch_time = at
        if at < 0:
            raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))

        if not isinstance(target, LineSegments):
            raise (Exception("TypeError: Imitation between different species is not supported."))
        self._actions = target.copy_actions()
        self._delay = at - target.get_hatch_time()
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
        Parse pipes to states then to storyboard objects
        :return:
        """
        hatch_state = LineSegmentsState(self._hatch_time, self._actions["pos"].to_list()[0][2])
        following_states = {}

        for prop, pipe in self._actions.items():
            pipe = pipe.to_list()
            first_action = pipe[0]
            setattr(hatch_state, prop, first_action[2])
            for i in range(1, len(pipe)):
                if pipe[i][0] not in following_states.keys():
                    following_states[pipe[i][0]] = LineSegmentsState(pipe[i][0], self._actions["pos"]
                                                                     .get_latest_value(at=pipe[i][0]))
                setattr(following_states[pipe[i][0]], prop, pipe[i-1][2])
                if pipe[i][1] not in following_states.keys():
                    following_states[pipe[i][1]] = LineSegmentsState(pipe[i][1], self._actions["pos"]
                                                                     .get_latest_value(at=pipe[i][1]))
                setattr(following_states[pipe[i][1]], prop, pipe[i][2])
        ret = hatch_state.to_dict()
        ret["states"] = []
        for v in following_states.values():
            ret["states"].append(v.to_dict())
        return ret


if __name__ == '__main__':
    my_pos = [Vertex(x=-2, y=1), Vertex(x=2, y=1)]
    my_init = {
        "opacity": 1,
        "color": "#FFF",
        "width": 0.05,
    }
    line = LineSegments().hatch(at=10, pos=my_pos, init=my_init)\
        .morph(at=11, to_morph={"opacity": 0}, duration=1)
    print(line.to_storyboard())

"""
platform: any
env: any
name: Scene.py
note state (note controllers)
"""
from util.storyboard.base import ActionPipe, SwitchPipe, Animation
from copy import deepcopy


class NoteState:
    def __init__(self, time, easing):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        # basic params
        self.time = time  # absolute time
        self.easing = easing  # easing

        # override xyz-coord
        self.override_x = False                 # whether override x-coord of note
        self.x = None                           # override value, noteX coord sys
        self.x_multiplier = 1                   # multiplier on x
        self.dx = 0                             # delta on x, noteX coord sys
        self.override_y = False                 # whether override y-coord of note
        self.y = None                           # override value, noteY coord sys
        self.y_multiplier = 1                   # multiplier on y
        # [omo]tcha: add 1 to dy if notes lie in -1 direction chart pages
        self.dy = 0                             # delta on y, noteY coord sys
        self.override_z = False                 # whether override z-coord of note
        self.z = None                           # override value, depth coord sys

        # override rotation on xyz-axis
        self.override_rot_x = False             # whether override rotation on x-axis
        self.rot_x = 0                          # override value in degrees
        self.override_rot_y = False             # whether override rotation on y-axis
        self.rot_y = 0                          # override value in degrees
        self.override_rot_z = False             # whether override rotation on z-axis
        self.rot_z = 0                          # override value in degrees

        # colors
        self.override_ring_color = False        # whether override note ring color
        self.ring_color = None                  # override value, hex string
        self.override_fill_color = False        # whether override note fill color
        self.fill_color = None                  # override value, hex string

        # opacity
        self.opacity_multiplier = 1             # multiplier on note opacity

        # size: only works on clicks and flicks
        self.size_multiplier = 1                # multiplier on note size

        # override hold direction: only works on holds
        self.hold_direction = None              # 1 for hold extending upwards, -1 for hold extending downwards

        # hold style: only works on holds
        self.style = 1                          # 1 for default, 2 for VSRG effect


class NoteController:
    """
    A note controller can also enable/disable but can not been destroyed
    """

    def __init__(self, target, coord_sys="note"):
        """
        create a note controller object
        self._notes is  a list of note ids
        self._id is a unique id of an object
        self._current_state is the object lifecycle state
        self._hatch_time is when the object is hatched
        self._actions is the dictionary of action pipelines
        self._
        self._delay is used when imitating
        self._coord_sys is the coordinate system used in note position
        :param target:  notes target, it can be a list of integers(note id) or a note selector object
        :param coord_sys: the coordinate system type of note controller object, default: note
        """
        if isinstance(target, list):
            # [omo]tcha: Same with SceneObjects, notes in the list shares the same absolute timing
            # i.e. the NoteController here does not support $ placeholder for relative note time.
            # If you want to a list of notes of which the time based on themselves,
            # you can create a list of note controllers, one controller for one note,
            # of which all time are based on an absolute timetable generated by ChartAnalyzer
            for item in target:
                if not isinstance(item, int):
                    raise (Exception("ParameterError: Target should be a single or a list of note ids."))
            self._notes = target
        elif isinstance(target, int):
            self._notes = [target]
        else:
            raise (Exception("ParameterError: Target should be a single or a list of note ids."))

        self._id = "note_controller_" + str(id(self))
        self._current_state = "egg"
        self._hatch_time = 0
        self._actions = {}
        self._switches = {}
        self._delay = 0

        # [omo]tcha: here I limit some properties' ability to morph and move
        self._morphable_props = ["ring_color", "fill_color", "opacity_multiplier", "hold_direction", "style"]
        self._scalable_props = ["size_multiplier"]
        self._movable_props = ["x", "y"]
        self._rotatable_props = ["rot_x", "rot_y", "rot_z"]
        self._switchable_props = ["override_" + prop for prop in
                                  self._movable_props + self._rotatable_props + ["ring_color", "fill_color"]]

        if coord_sys in ["note", "stage"]:
            self._coord_sys = coord_sys
        else:
            raise (Exception("ParameterError: coord sys note or stage, {} found.".format(coord_sys)))

    def hatch(self, at, init=None):
        """
        The concept of note controller is more alike note, therefore it has hatch function
        It should be the first action(or state change) of an object.
        After that, the object's state is "active" and listens for next action
        :param at: when to hatch (absolute time)
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
                                + self._scalable_props + self._movable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    for k in init.keys():
                        self._actions[k] = ActionPipe(at, init[k])
                    for k in self._switchable_props:
                        # [omo]tcha: in note controllers, all switchable properties start with "override_"
                        if k.split("_")[1] in init.keys():
                            self._switches[k] = SwitchPipe(at, True)
                        else:
                            self._switches[k] = SwitchPipe(at, False)
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
        :param to: where to move to ((x, y) in noteXY|StageXY coord sys)
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
                self._switches["override_x"].add(at, value=True)
                self._actions["x"].add(at, duration=duration, value=to[0], easing=easing)

            if to[1] is not None:
                if "y" not in self._actions.keys():
                    self._actions["y"] = ActionPipe(self._hatch_time, to[1])
                self._switches["override_y"].add(at, value=True)
                self._actions["y"].add(at, duration=duration, value=to[1], easing=easing)

        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def rotate(self, at, axis, degree, duration, animation=None):
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

            prop = "rot_{}".format(axis)
            if prop not in self._actions.keys():
                self._actions[prop] = ActionPipe(self._hatch_time, degree)
            self._switches["override_" + prop].add(at, value=True)
            self._actions[prop].add(at, duration=duration, value=degree, easing=easing)

            # [omo]tcha: seems pivots are not settable
            # if axis == "x" or axis == "y" and pivot is not None:
            #     prop = "pivot_{}".format(axis)
            #     if prop not in self._actions.keys():
            #         self._actions[prop] = ActionPipe(self._hatch_time, pivot)
            #     self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)

        else:
            raise (Exception("ActionError: The object is not active: {}.".format(self._id)))
        return self

    def scale(self, at, value, duration, animation=None):
        """
        Change scaling-related state property of an active object
        :param at: when to scale (absolute time)
        :param value: scaling factor
        :param duration: how long to move (time)
        :param animation: how to move (Animation indicating easing)
        :return:
        """
        if self._current_state == "active":
            if at < self._hatch_time:
                raise (Exception("ValueError: Time should be greater than _hatch_time, but have {}.".format(at)))
            if duration < 0:
                raise (Exception("ValueError: Duration should be greater than 0, but have {}".format(duration)))

            easing = animation.easing if animation is not None else "linear"

            if "size_multiplier" not in self._actions.keys():
                self._actions["size_multiplier"] = ActionPipe(self._hatch_time, value)
            self._actions["size_multiplier"].add(at, duration=duration, value=value, easing=easing)

            # [omo]tcha: seems pivots are not settable
            # if pivot is not None:
            #     if axis != "x":
            #         prop = "pivot_y"
            #         if prop not in self._actions.keys():
            #             self._actions[prop] = ActionPipe(self._hatch_time, pivot)
            #         self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)
            #     if axis != "y":
            #         prop = "pivot_x"
            #         if prop not in self._actions.keys():
            #             self._actions[prop] = ActionPipe(self._hatch_time, pivot)
            #         self._actions[prop].add(at, duration=duration, value=pivot, easing=easing)

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
                        if k in ["ring_color", "fill_color"]:
                            self._switches["override_" + k].add(at, value=True)
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
        Current note controller follows another note controller.
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

        if not isinstance(target, NoteController):
            raise (Exception("TypeError: Imitation between different species is not supported."))
        self._actions = target.copy_actions()
        self._switches = target.copy_switches()
        self._delay = at - target.get_hatch_time()
        return self

    def get_hatch_time(self):
        return self._hatch_time

    def copy_actions(self):
        ret = {}
        for k, v in self._actions.items():
            ret[k] = deepcopy(v)
        return ret

    def copy_switches(self):
        ret = {}
        for k, v in self._switches.items():
            ret[k] = deepcopy(v)
        return ret

    def enable(self, prop, at):
        """
        set a switchable property to true at some time
        :param prop: property
        :param at: absolute time
        :return:
        """
        if at < 0:
            raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
        if prop not in self._switchable_props:
            raise (Exception("ValueError: Property {} is not switchable".format(prop)))
        if prop not in self._switches.keys():
            self._switches[prop] = SwitchPipe(at, True)
        else:
            self._switches[prop].add(at, True)
        return self

    def disable(self, prop, at):
        """
        set a switchable property to false at some time
        :param prop: property
        :param at: absolute time
        :return:
        """
        if at < 0:
            raise (Exception("ValueError: Time should be greater than 0, but have {}.".format(at)))
        if prop not in self._switchable_props:
            raise (Exception("ValueError: Property {} is not switchable".format(prop)))
        if prop not in self._switches.keys():
            self._switches[prop] = SwitchPipe(at, False)
        else:
            self._switches[prop].add(at, False)
        return self

    def to_storyboard(self):
        """
        Parse object to storyboard object
        :return:
        """
        ret = []
        for prop, action_pipe in self._actions.items():
            action_pipe = action_pipe.to_list()
            prop_states = {
                action_pipe[0][0]: {
                    "time": action_pipe[0][0],
                    prop: "stage{}:{}".format(prop.upper(), action_pipe[0][2])
                    if prop in ["x", "y"] and self._coord_sys == "stage" else action_pipe[0][2],
                    "easing": action_pipe[0][3]
                }
            }
            for i in range(1, len(action_pipe)):
                prop_states[action_pipe[i][0] + self._delay] = {
                    "time": action_pipe[i][0] + self._delay,
                    prop: "stage{}:{}".format(prop.upper, action_pipe[i-1][2])
                    if prop in ["x", "y"] and self._coord_sys == "stage" else action_pipe[i-1][2],
                    "easing": action_pipe[i][3]
                }
                prop_states[action_pipe[i][1] + self._delay] = {
                    "time": action_pipe[i][1] + self._delay,
                    prop: "stage{}:{}".format(prop.upper, action_pipe[i][2])
                    if prop in ["x", "y"] and self._coord_sys == "stage" else action_pipe[i][2],
                    "easing": action_pipe[i-1][3]
                }

            if "override_" + prop in self._switchable_props:
                switch_pipe = self._switches["override_" + prop].to_list()
                for state in switch_pipe:
                    if state[0] + self._delay in prop_states.keys():
                        prop_states[state[0]+self._delay]["override_"+prop] = state[1]
                    else:
                        prop_states[state[0] + self._delay] = {
                            "time": state[0]+self._delay,
                            "override_" + prop: state[1]
                        }
            ret.append({
                "note": self._notes,
                "states": [v for _, v in prop_states.items()]
            })
        return ret


if __name__ == '__main__':
    ani = Animation()
    ani.easing = "easeInQuad"
    nc = NoteController(target=[1, 2], coord_sys="note")\
        .hatch(at=1, init={"x": 0.5})\
        .disable("override_x", 10)\
        .move(at=11, to=(1, 2), duration=1, animation=ani)
    print(nc.to_storyboard())

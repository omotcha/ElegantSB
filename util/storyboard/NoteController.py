"""
platform: any
env: any
name: Scene.py
note state (note controllers)
"""
from util.storyboard.base import ActionPipe, NoteSelector


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
    A note controller can not been destroyed
    """

    def __init__(self, target):
        """
        create a note controller object
        self._notes are notes target
        self._id is a unique id of an object
        self._current_state is the object lifecycle state
        self._hatch_time is when the object is hatched
        self._actions is the dictionary of action pipelines
        self._delay is used when imitating
        :param target:  notes target, it can be a list of integers(note id) or a note selector object
        """
        if isinstance(target, list):
            for item in target:
                if not isinstance(item, int):
                    raise (Exception("ParameterError: Target should be a list of integers or a note selector object."))
            self._notes = target
        elif isinstance(target, int):
            self._notes = target
        elif isinstance(target, NoteSelector):
            self._notes = target.to_dict()
        else:
            raise (Exception("ParameterError: Target should be a list of integers or a note selector object."))

        self._id = "note_controller_" + str(id(self))
        self._current_state = "egg"
        self._hatch_time = 0
        self._actions = {}
        self._delay = 0

        # [omo]tcha: here I limit some properties' ability to morph
        self._morphable_props = []
        self._scalable_props = []
        self._movable_props = []
        self._rotatable_props = []

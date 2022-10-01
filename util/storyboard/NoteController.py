"""
platform: any
env: any
name: Scene.py
note state (note controllers)
"""


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

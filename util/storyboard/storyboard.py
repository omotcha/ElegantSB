"""
platform: any
env: any
name: storyboard.py
storyboard and member objects
reference: https://www.notion.so/Full-Specification-4aece3f705d0485495b64564167e76ce
"""
import json


class Vertex:
    def __init__(self):
        self.x = 0                              # stageX coord sys
        self.y = 0                              # stageY coord sys
        self.z = 0                              # depth coord sys


class NoteSelector:
    def __init__(self):
        self.type = []                          # list of acceptable note types
        self.start = None                       # start id of note
        self.end = None                         # end id of note
        self.direction = None                   # 1 for notes scanned upwards, -1 for notes scanned downwards
        self.min_x = None                       # minimum x-coord of note
        self.max_x = None                       # maximum x-coord of note


class SceneObjectState:
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """

        # basic params
        self.time = time                        # absolute time
        self.easing = easing                    # easing
        self.destroy = False                    # destroy

        # placing
        self.x = 0                              # stageX coord sys
        self.y = 0                              # stageY coord sys
        self.z = 0                              # depth coord sys

        # rotating
        self.rot_x = 0                          # degrees
        self.rot_y = 0                          # degrees
        self.rot_z = 0                          # degrees

        # scaling
        self.scale_x = 1                        # scale on x-axis
        self.scale_y = 1                        # scale on y-axis
        self.scale = 1                          # scale on both x and y-axis

        # pivot for rotating/scaling
        self.pivot_x = 0.5                      # 0 for left, 1 for right, 0.5 for center
        self.pivot_y = 0.5                      # 0 for left, 1 for right, 0.5 for center

        # opacity
        self.opacity = 0                        # 0 for invisible, 1 for visible

        # size
        self.width = 200                        # for sprites
        self.height = 200                       # for sprites

        # layer placing
        # 0 for background | obj | other game elements | ui
        # 1 for background | other game elements | obj | ui
        # 2 for background | other game elements | ui | obj
        self.layer = 0
        self.order = 0                          # higher ordered obj will display more in front

        # stretching
        self.fill_width = False                 # if True, width <- stage's width, height <- 10000


class TextState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        # self.text = ""                          # text string
        self.color = "#FFF"                     # hex string
        self.size = 20                          # font size, integer
        self.align = "middleCenter"             # upper|middle|lower + Left|Center|Right
        self.letter_spacing = 0                 # letter spacing
        self.font_weight = "regular"            # regular|extraLight|bold|extraBold


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


class VideoState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.path = ""                          # relative path to video
        self.color = "#FFF"                     # hex string for tint color


class LineState(SceneObjectState):
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        super().__init__(time, easing)
        self.pos = []                           # list of Vertex
        self.width = 0.05
        self.color = "#FFF"                     # hex string


class SceneState:
    def __init__(self, time, easing="linear"):
        """

        :param time:    [omo]tcha: here I limit the functionality of time, only absolute time is used
        :param easing:
        """
        # basic params
        self.time = time  # absolute time
        self.easing = easing  # easing

        # opacity and dim
        self.storyboard_opacity = 1             # opacity of all storyboard scene objects
        self.ui_opacity = 1                     # opacity of game ui
        self.scanline_opacity = 1               # opacity of scanline
        self.background_dim = 0.85              # opacity of background dim
        self.note_opacity_multiplier = 1        # multiplier on note opacity

        # color
        self.scanline_color = None              # override the scanline color
        self.note_ring_color = None             # override the note ring color
        # override the note fill colors
        # [click 1, click 2, drag 1, drag 2,
        #  hold 1,  hold 2,  l-hold 1, l-hold 2,
        #  flick 1, flick 2, c-drag 1, c-drag 2]
        self.note_fill_colors = None

        # scanline reposition
        self.override_scanline_pos = False      # whether override the scanline position
        self.scanline_pos = 0                   # override the scanline y-coord, value falls into [0-1], noteY coord sys

        # camera param
        self.perspective = True                 # uses a perspective camera if True otherwise an orthographic camera

        # larger size -> smaller scene
        self.size = 5                           # the viewport size of orthographic camera, require perspective <- false

        # larger fov -> smaller scene
        self.fov = 53.2                         # field of view of perspective camera, require perspective <- true

        # larger x -> "left"er shift of scene
        self.x = 0                              # x-coord of camera, cameraX coord sys

        # larger y -> "bottom"er shift of scene
        self.y = 0                              # y-coord of camera, cameraY coord sys

        # larger z -> closer
        self.z = -10                            # z-coord of camera, depth coord sys

        # rotating
        self.rot_x = 0                          # rotation of camera along with x-axis
        self.rot_y = 0                          # rotation of camera along with y-axis
        self.rot_z = 0                          # rotation of camera along with z-axis

        #####################################
        # [omo]tcha: effects-related
        #####################################

        # chromatic aberration
        self.chromatical = False
        self.chromatical_fade = 0               # transparency, value falls into [0,1]
        self.chromatical_intensity = 0          # intensity, value falls into [0,1]
        self.chromatical_speed = 0              # speed, value falls into [0,3]

        # bloom
        self.bloom = False
        self.bloom_intensity = 0                # intensity, value falls into [0,5]

        # radial blur
        self.radial_blur = False
        self.radial_blur_intensity = 0.025      # intensity, value falls into [-0.5,0.5]

        # color adjustment
        self.color_adjustment = False
        self.brightness = 1                     # brightness, value falls into [0,10]
        self.saturation = 1                     # saturation, value falls into [0,10]
        self.contrast = 1                       # contrast, value falls into [0,10]

        # screen color filter
        self.color_filter = False
        self.color_filter_color = "#FFF"        # filter color, hex string

        # grey scale
        self.grey_scale = False
        self.grey_scale_intensity = 0           # intensity, value falls into [0,1]

        # noise
        self.noise = False
        self.noise_intensity = 0.235            # intensity, value falls into [0,1]

        # sepia
        self.sepia = False
        self.sepia_intensity = 0                # intensity, value falls into [0,1]

        # dream
        self.dream = False
        self.dream_intensity = 0                # intensity, value falls into [0,1]

        # fisheye
        self.fisheye = False
        self.fisheye_intensity = 0.5            # intensity, value falls into [0,1]

        # shockwave
        self.shockwave = False
        self.shockwave_speed = 1                # speed, value falls into [0,10]

        # focus line
        self.focus = False
        self.focus_size = 1                     # size, value falls into [0,10]
        self.focus_color = "#FFF"               # color of focus line, hex string
        self.focus_speed = 5                    # speed, value falls into [0,30]
        self.focus_intensity = 0.25             # intensity, value falls into [0,1]

        # glitch
        self.glitch = False
        self.glitch_intensity = 0               # intensity, value falls into [0,1]

        # arcade screen
        self.arcade = False
        self.arcade_intensity = 1               # intensity, value falls into [0,1]
        self.arcade_interference_size = 1       # size of interference, value falls into [0,10]
        self.arcade_interference_speed = 0.5    # speed of interference, value falls into [0,10]
        self.arcade_contrast = 1                # contrast, value falls into [0,10]

        # tape(screen flipping)
        self.tape = False


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


class SceneObject:
    def __init__(self):
        self.id = str(id(self))
        self.states = []

    def appear(self, time, at, speed, animation):
        """
        It should be the first "action"(or state change) of an object.
        After that, the object's state will be frozen
        :param time: when to appear(absolute time)
        :param at: where to appear(x, y in stageXY coord sys)
        :param speed: how fast to appear
        :param animation: how to appear
        :return:
        """
        print("a scene object appears")
        return self

    def disappear(self, time, speed, animation):
        """
        It should be the last "action"(or state change) of an object.
        After that, the object will be destroyed
        :param time: when to disappear(absolute time)
        :param speed: how fast to disappear
        :param animation: how to disappear
        :return:
        """
        print("a scene object disappears")
        return self

    def move_to(self, time, at, speed, animation):
        """
        It should be called after the object appears and before it disappears
        :param time: when to move(absolute time)
        :param at: where to move to(x, y in stageXY coord sys)
        :param speed: how fast to move
        :param animation: how to move
        :return:
        """
        return self

    def to_json(self):
        return json.dumps(self)


class Text(SceneObject):
    def __init__(self, text_content):
        """

        :param text_content:
        """
        super().__init__()
        self.text = text_content
        self.id = "text_" + self.id

    def appear(self, time, at, speed, animation):
        print("a text object appears")
        return self


class StoryBoard:
    def __init__(self):
        self.texts = []                     # list of Text
        self.sprites = []                   # list of Sprite
        self.lines = []                     # list of Line
        self.videos = []                    # list of video
        self.controllers = []               # list of (scene)controller
        self.note_controllers = []          # list of note controller
        self.templates = []                 # list of template


if __name__ == '__main__':
    t_hello = Text("hello")
    print(t_hello.appear(None, None, None, None).disappear(None, None, None))


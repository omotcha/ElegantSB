"""
platform: any
env: any
name: Scene.py
scene state (controllers)
"""


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

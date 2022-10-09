"""
platform: any
env: any
name: Scene.py
scene state (controllers)
"""
from util.storyboard.base import ActionPipe, NoteFillColors


class SceneState:
    """
    SceneState is large and should be divided and limited maybe, so it actually serves as nothing.
    So better not use it directly or even override it.
    """
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


class SceneController:
    """
    [omo]tcha: SceneController just looks like an interface, of which the actions are not fully implemented.
    So do not use it directly unless you implement it yourself.
    A scene controller can only hatch, morph and mutate
    """
    def __init__(self):
        """
        self._id is a unique id of an object
        self._current_state is the object lifecycle state
            different from SceneObject, SceneController only have "hatched"/"unhatched" state
        self._hatch_time is when the object is hatched
        self._actions is the dictionary of action pipelines
            different from SceneObject, SceneController's action pipelines are determined and created in __init__
            but here initialization of action pipelines is not implemented
            cuz SceneController should not be used directly
        """
        self._id = "scene_controller_" + str(id(self))
        self._current_state = "egg"
        self._hatch_time = 0
        self._actions = {}

        # [omo]tcha: here I limit some properties' ability to morph
        self._morphable_props = []

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

    def to_storyboard(self):
        """
        Parse object to storyboard object, do not use it directly
        :return:
        """
        ret = []
        for prop, pipe in self._actions.items():
            pipe = pipe.to_list()
            dic = {
                "states": [{
                    "time": pipe[0][0],
                    prop: pipe[0][2],
                    "easing": pipe[0][3]
                }]
            }
            for i in range(1, len(pipe)):
                dic["states"].append({
                    "time": pipe[i][0],
                    prop: pipe[i-1][2],
                    "easing": pipe[i][3]
                })
                dic["states"].append({
                    "time": pipe[i][1],
                    prop: pipe[i][2],
                    "easing": pipe[i-1][3]
                })
            ret.append(dic)
        return ret


class UIController(SceneController):
    """
    UIController controls overall storyboard/background/ui elements, it does not control notes/scanline
    """
    def __init__(self, init=None):
        """

        :param init: initialized state (dict)
        """
        super().__init__()
        self._id = "ui_controller_" + self._id
        self._morphable_props += ["storyboard_opacity", "ui_opacity", "background_dim"]
        self.hatch(init)

    def hatch(self, init=None):
        """
        hatch function of UIController
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            if init is not None:
                if isinstance(init, dict):
                    for k in init.keys():
                        # [omo]tcha: init can be regarded as the first morph
                        if k not in self._morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    for k in init.keys():
                        self._actions[k] = ActionPipe(0, init[k])
                else:
                    raise (Exception("ParameterError: init should be a dictionary."))
            self._current_state = "active"
        else:
            raise (Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
        return self


class GlobalNoteController(SceneController):
    """
    GlobalNoteController controls overall note color and opacity, it can be overridden by note controller
    """
    def __init__(self, init=None):
        """

        :param init: initialized state (dict)
        """
        super().__init__()
        self._id = "global_note_controller" + self._id
        self._morphable_props += ["note_opacity_multiplier", "note_ring_color", "note_fill_colors"]
        self.hatch(init)

    def hatch(self, init=None):
        """
        hatch function of GlobalNoteController
        :param init: initialized state (dict)
        :return:
        """
        if self._current_state == "egg":
            if init is not None:
                if isinstance(init, dict):
                    for k in init.keys():
                        # [omo]tcha: init can be regarded as the first morph
                        if k not in self._morphable_props:
                            raise (Exception("KeyError: Key {} cannot be used for initializing.".format(k)))
                    for k in init.keys():
                        self._actions[k] = ActionPipe(0, init[k])
                else:
                    raise (Exception("ParameterError: init should be a dictionary."))
            self._current_state = "active"
        else:
            raise (Exception("ActionError: The object has been hatched before: {}.".format(self._id)))
        return self

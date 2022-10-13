"""
platform: any
env: any
name: Templates.py
ESB built-in templates
"""
from util.storyboard.base import Animation
from util.storyboard.Scene import *


def beat(target=None, at=None, intensity=1, animation=Animation()):
    """
    pulsing effect
    :param target:  as default, we add pulsing effect to a perspective camera object,
                    an orthographic camera is also supported,
                    if it is none, we will create a new one
    :param at: list of absolute time
    :param intensity: intensity of pulsing effect, ranging from 0 to 10
    :param animation: how to beat, use its mutate_interval
    :return:
    """
    if at is None:
        at = []
    if not isinstance(at, list):
        at = [at]

    if target is None:
        target = PerspectiveCameraController({"fov": 53.2})
    elif isinstance(target, PerspectiveCameraController) or isinstance(target, OrthographicCameraController):
        pass
    else:
        raise (Exception("TypeError: Only CameraController and its subclass are expected for target type."))

    if isinstance(target, PerspectiveCameraController):
        prop = "fov"
        value = round(53.2+intensity/5, 1)
    else:
        prop = "size"
        value = round(5+intensity/5, 1)

    for time in at:
        target = target.mutate(at=time, to_mutate={prop: value}, animation=animation)

    return target


if __name__ == '__main__':
    camera = OrthographicCameraController({"size": 5})
    print(camera.to_storyboard())
    camera = beat(camera, at=[1, 11, 21, 31], intensity=1, animation=Animation())
    print(camera.to_storyboard())

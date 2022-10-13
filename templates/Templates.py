"""
platform: any
env: any
name: Templates.py
ESB built-in templates
"""
from util.storyboard.base import Animation
from util.storyboard.Scene import *


def beat(target=None, timetable=None, intensity=1, animation=Animation()):
    """
    pulsing effect
    :param target:  as default, we add pulsing effect to a perspective camera object,
                    orthographic camera and base camera are also welcomed,
                    if it is none, we will create a new one
    :param timetable: list of time
    :param intensity: intensity of pulsing effect, ranging from 0 to 10
    :param animation: how to beat, use its mutate_interval
    :return:
    """
    if target is None or isinstance(target, CameraController):
        target = PerspectiveCameraController({"fov": 53.2})
    elif isinstance(target, PerspectiveCameraController) or isinstance(target, OrthographicCameraController):
        pass
    else:
        raise (Exception("TypeError: Only CameraController and its subclass are expected for target type."))

    if timetable is None:
        timetable = []
    if not isinstance(timetable, list):
        timetable = [timetable]

    if isinstance(target, PerspectiveCameraController):
        prop = "fov"
        value = round(53.2+intensity/5, 1)
    else:
        prop = "size"
        value = round(5+intensity/5, 1)

    for time in timetable:
        target = target.mutate(at=time, to_mutate={prop: value}, animation=animation)

    return target


if __name__ == '__main__':
    camera = PerspectiveCameraController({"fov": 53.2}).enable_at(0)

    print(camera.to_storyboard())
    camera = beat(camera, timetable=[1, 11, 21, 31], intensity=1, animation=Animation())
    print(camera.to_storyboard())

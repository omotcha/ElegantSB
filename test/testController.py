"""
platform: any
env: any
name: testController.py
Tester of Scene Controller object
"""

import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Scene import *
from util.storyboard.base import Animation, NoteFillColors
from util.storyboard.Storyboard import StoryBoard


def test():
    storyboard = StoryBoard()
    animation = Animation()
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    t = analyzer.get_note_times()
    ui_controller = UIController(init={"storyboard_opacity": 1, "ui_opacity": 1, "background_dim": 0.85})\
        .morph(at=t[19], to_morph={"storyboard_opacity": 0}, duration=4)\
        .mutate(at=t[39], to_mutate={"ui_opacity": 0.5}, animation=animation)
    global_note_controller = GlobalNoteController(init={"note_opacity_multiplier": 0.5})\
        .morph(at=t[39], to_morph={"note_opacity_multiplier": 1}, duration=4)\
        .morph(at=t[39], to_morph={"note_fill_colors": NoteFillColors().to_list()}, duration=4)
    scanline_controller = ScanlineController(init={"override_scanline_pos": False})\
        .morph(at=t[10], to_morph={"override_scanline_pos": True, "scanline_pos": 0.5}, duration=1)
    perspective_camera_controller = PerspectiveCameraController(init={"perspective": True, "fov": 53.2})\
        .mutate(at=t[20], to_mutate={"fov": 55.2}, animation=animation)
    chromatical_effect = Chromatical(init={"chromatical": False, "chromatical_intensity": 0})\
        .morph(at=t[19], to_morph={"chromatical": True, "chromatical_intensity": 0.5}, duration=1)
    storyboard.add(chromatical_effect)
    # storyboard.add(perspective_camera_controller)
    # storyboard.add(ui_controller)
    # storyboard.add(global_note_controller)
    # storyboard.add(scanline_controller)
    print(storyboard.parse())


if __name__ == '__main__':
    test()

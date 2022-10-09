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
from util.storyboard.base import Animation
from util.storyboard.Storyboard import StoryBoard


def test():
    storyboard = StoryBoard()
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    t = analyzer.get_note_times()
    ui_controller = UIController(init={"storyboard_opacity": 1, "ui_opacity": 1, "background_dim": 0.85})\
        .morph(at=t[19], to_morph={"storyboard_opacity": 0}, duration=4)\
        .mutate(at=t[39], to_mutate={"ui_opacity": 0.5}, animation=Animation())
    storyboard.add(ui_controller)
    print(storyboard.parse())


if __name__ == '__main__':
    test()

"""
platform: any
env: any
name: testNoteController.py
Tester of Note Controller object
"""

import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.NoteController import *
from util.storyboard.base import Animation, NoteFillColors
from util.storyboard.Storyboard import StoryBoard

storyboard = StoryBoard()
ani = Animation()
ani.easing = "easeInQuad"
analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
t = analyzer.get_note_times()
morphable_props = ["ring_color", "fill_color", "opacity_multiplier", "hold_direction", "style"]
scalable_props = ["size_multiplier"]
movable_props = ["x", "y"]
rotatable_props = ["rot_x", "rot_y", "rot_z"]
hatchable_props = movable_props + morphable_props + scalable_props + rotatable_props
default_state = NoteState(time=0, easing=ani.easing)


def testInitAndHatch():
    # all props should be hatchable and should be hatched to a proper value
    for prop in hatchable_props:
        nc = NoteController(target=1, coord_sys="note").hatch(at=0, init={prop: default_state.__getattribute__(prop)})
        print(nc.to_storyboard())


def test():
    note_controller = NoteController(target=1, coord_sys="stage")\
        .hatch(at=1, init={"x": 200})\
        .disable("override_x", 10)\
        .move(at=11, to=(100, 200), duration=1, animation=ani)
    print(note_controller.to_storyboard())


if __name__ == '__main__':
    test()

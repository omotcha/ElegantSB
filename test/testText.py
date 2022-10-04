"""
platform: any
env: any
name: testText.py
Tester of Text object
"""

import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Text import *
from util.storyboard.base import Animation
from util.storyboard.Storyboard import StoryBoard


def test():
    my_storyboard = StoryBoard()
    ani = Animation()
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    t = analyzer.get_note_times()
    init = {
        "color": "#FFF",
        "opacity": 0,
        "rot_z": 0,
        "scale": 1,
        "pivot_x": 0.5,
        "pivot_y": 0.5
    }
    nhelv_text = Text(r"NHELV").hatch(at=t[19], init=init) \
        .morph(at=t[19], to_morph={"opacity": 1}, duration=4) \
        .rotate(at=t[21], axis="z", degree=90, duration=11) \
        .scale(at=t[46], axis="xy", value=1.5, duration=5, pivot=1) \
        .mutate(at=t[39], to_mutate={"scale": 3}, animation=ani)
    my_storyboard.add(nhelv_text)
    sltrm_text = Text(r"SilentRoom").imitate(at=t[19], target=nhelv_text)\
        .move(at=t[19], to=(0, -150), duration=0)\
        .destroy(at=t[100])
    my_storyboard.add(sltrm_text)
    print(my_storyboard.parse())


if __name__ == '__main__':
    test()

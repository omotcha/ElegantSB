"""
platform: any
env: any
name: testSprite.py
Tester of Sprite object
"""

import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Sprite import *
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
    whale_one = Sprite("one.png").hatch(at=t[19], init=init) \
        .morph(at=t[19], to_morph={"opacity": 1}, duration=4) \
        .rotate(at=t[21], axis="z", degree=90, duration=11) \
        .scale(at=t[46], axis="xy", value=1.5, duration=5, pivot=1) \
        .mutate(at=t[39], to_mutate={"scale": 3}, animation=ani)
    my_storyboard.add(whale_one)
    whale_two = Sprite("two.png").imitate(at=t[19], target=whale_one) \
        .move(at=t[19], to=(0, -150), duration=0) \
        .destroy(at=t[100])
    my_storyboard.add(whale_two)
    print(my_storyboard.parse())


if __name__ == '__main__':
    test()

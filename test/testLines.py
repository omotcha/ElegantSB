"""
platform: any
env: any
name: testLines.py
Tester of Line Segments object
"""

import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Line import *
from util.storyboard.base import Vertex
from util.storyboard.Storyboard import StoryBoard


def test():
    storyboard = StoryBoard()
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    t = analyzer.get_note_times()
    for i in range(16):
        init_pos = [Vertex(x=-1.5, y=1-i/16), Vertex(x=1.5, y=1-i/16)]
        color = str(hex(220-i*7))[2:].upper()
        init = {
            "opacity": 0,
            "color": "#FF{}{}".format(color, color),
            "width": 0.05,
        }
        new_pos = [Vertex(x=1.2, y=2), Vertex(x=1.2, y=-2)]
        sample_line = LineSegments().hatch(at=t[271+i]-0.05, pos=init_pos, init=init) \
            .morph(at=t[271+i], to_morph={"opacity": 1}, duration=0.35) \
            .move(at=t[271+i], shift=(0, -1/16), duration=0.35-i/100)\
            .morph(at=t[271+i]+0.35-i/100, to_morph={"pos": new_pos, "color": "#FFCDCD"}, duration=0.15-i/200) \
            .destroy(at=t[271+i]+0.7)
        storyboard.add(sample_line)
    print(storyboard.parse())


if __name__ == '__main__':
    test()

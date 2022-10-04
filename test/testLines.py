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
    my_storyboard = StoryBoard()
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    t = analyzer.get_note_times()
    init_pos = [Vertex(x=-2, y=0.5), Vertex(x=2, y=0.5)]
    init = {
        "opacity": 1,
        "color": "#FFFFFF",
        "width": 0.3,
    }
    sample_line = LineSegments().hatch(at=t[271]-0.05, pos=init_pos, init=init)\
        .morph(at=t[271], to_morph={"opacity": 0}, duration=1)\
        .move(at=t[271], shift=(0, -1/8), duration=0.2)

    my_storyboard.add(sample_line)
    print(my_storyboard.parse())


if __name__ == '__main__':
    test()

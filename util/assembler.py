"""
platform: any
env: any
name: Storyboard.py
this is the programming interface in Iter1
"""
import os
from configs.config import example_dir
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Text import Text, TextState
from util.storyboard.base import Animation
from util.storyboard.Storyboard import StoryBoard


def assemble():

    # first we create a storyboard object
    my_storyboard = StoryBoard()

    # second we create a linear animation widget
    ani = Animation()

    # chart analyzer is a helpful tool to get important information, e.g. absolute time
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))

    # here we generate the absolute time of all notes (counting from 0) and store them to list "t"
    t = analyzer.get_note_times()

    # We might want to hatch a text with an initialized parameters like this:
    init = {
        "color": "#FFF",
        "opacity": 0,
        "rot_z": 0,
        "scale": 1,
        "pivot_x": 0.5,
        "pivot_y": 0.5
    }

    # Or we can just get all parameters initialized with default values like this:
    # init = TextState(t[19]).init()

    # After hatching, we append a morph action followed by a rotation, a morph, and a mutation to the object.
    # The first morph action starts at the 20th note, it changes the opacity from 0 to 1  in 4 seconds.
    # The rotation action starts at the 22nd note, it rotates the text along z-axis for 90 degrees in 10 seconds.
    # The second morph action starts at the 46th note, it scales the text to 1.5x the original size in 5 seconds.
    # The mutate action starts at the 39th note,
    # it scales the text to 3x the original size in a sudden then scales back.
    # here "hatch" is similar with "initialize", and "morph" is similar with "state change"
    # P.S. here "t[19]" is similar with "start:19", "t[a]+b" is similar with "start:a:b"

    elegant_text = Text(r"NHELV").hatch(at=t[19], init=init)\
        .morph(at=t[19], to_morph={"opacity": 1}, duration=4)\
        .rotate(at=t[21], axis="z", degree=90, duration=11)\
        .scale(at=t[46], axis="xy", value=1.5, duration=5, pivot=1)\
        .mutate(at=t[39], to_mutate={"scale": 3}, animation=ani)

    # when everything is done with our elegant text, we add it to our storyboard
    my_storyboard.add(elegant_text)

    # finally, parse the storyboard to JSON
    print(my_storyboard.parse())
    return my_storyboard.parse()


if __name__ == '__main__':
    assemble()

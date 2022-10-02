"""
platform: any
env: any
name: Storyboard.py
this is the programming interface in Iter1
"""
from configs.config import example_dir
import os
from util.storyboard.Storyboard import StoryBoard
from util.chart.analyzer import ChartAnalyzer
from util.storyboard.Text import Text


def assemble():

    # first we create a storyboard object
    my_storyboard = StoryBoard()

    # chart analyzer is a helpful tool to get important information, e.g. absolute time
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))

    # here we get the absolute time of the 18th note (counting from 0) and store the time value to "t"
    t = analyzer.get_time(query=17, by="note_id")

    # then we add a text object "elegant" and hatch it at time t with color "#F00"
    # here "hatch" is similar with "initialize", and as a result, it creates a text with 0 opacity
    elegant_text = Text(r"elegant").hatch(at=t, init={"color": "#F00"})

    # when everything is done with our elegant text, we add it to our storyboard
    my_storyboard.add(elegant_text)

    # finally, parse the storyboard to JSON
    print(my_storyboard.parse())


if __name__ == '__main__':
    assemble()

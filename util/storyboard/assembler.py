"""
platform: any
env: any
name: storyboard.py
assemble components of a storyboard and associate with given chart
"""
from util.storyboard.storyboard import StoryBoard
from util.chart.analyzer import Chart


class StoryBoardAssembler:
    def __init__(self, chart_f):
        self._chart = Chart(chart_f)
        self._storyboard = StoryBoard()

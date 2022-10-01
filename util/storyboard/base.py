"""
platform: any
env: any
name: base.py
base classes
"""


class Vertex:
    def __init__(self):
        self.x = 0                              # stageX coord sys
        self.y = 0                              # stageY coord sys
        self.z = 0                              # depth coord sys


class Animation:
    def __init__(self):
        self.type = None
        self.easing = "linear"


class NoteSelector:
    def __init__(self):
        self.type = []                          # list of acceptable note types
        self.start = None                       # start id of note
        self.end = None                         # end id of note
        self.direction = None                   # 1 for notes scanned upwards, -1 for notes scanned downwards
        self.min_x = None                       # minimum x-coord of note
        self.max_x = None                       # maximum x-coord of note

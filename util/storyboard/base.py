"""
platform: any
env: any
name: base.py
base classes
"""
from bisect import bisect_right

MAX_PIPE_TIME = 10000


class Vertex:
    def __init__(self, x, y, z=None):
        self.x = x  # stageX coord sys
        self.y = y  # stageY coord sys
        self.z = 0 if z is None else z  # depth coord sys


class Animation:
    def __init__(self):
        self.type = None
        self.mutate_interval = 0.05
        self.easing = "linear"


class NoteSelector:
    def __init__(self):
        self.type = []  # list of acceptable note types
        self.start = None  # start id of note
        self.end = None  # end id of note
        self.direction = None  # 1 for notes scanned upwards, -1 for notes scanned downwards
        self.min_x = None  # minimum x-coord of note
        self.max_x = None  # maximum x-coord of note


class ActionPipe:
    """
    [omo]tcha: ActionPipe is a data structure to store and manage actions.
    Here action is minimized upon a single property.
    ActionPipe maintains a list of tuples (start_time, end_time, value of property, easing type)
    that each time period (from start_time to end_time) cannot overlap with each other.
    For simplicity, I use a dictionary with action start_time as keys instead.
    """

    def __init__(self, hatch_time, hatch_value):
        """
        The first action should be "hatch" action, with start_time equals end_time
        :param hatch_time:
        :param hatch_value:
        """
        if hatch_time < 0 or hatch_time >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid hatch time: {}".format(hatch_time)))
        self._pipe = {hatch_time: (hatch_time, hatch_time, hatch_value, "linear")}
        self._hatch_time = hatch_time

    def add(self, at, duration, value, easing):
        """
        Add an action to the pipe
        :param at: start_time (absolute time)
        :param duration: end_time - start_time
        :param value: value of property
        :param easing: easing type
        :return:
        """
        if at < self._hatch_time or at + duration >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid time period: {} - {}".format(at, at + duration)))
        key_list = list(self._pipe.keys())
        bi = bisect_right(key_list, at)
        if bi:
            if at >= self._pipe[key_list[bi - 1]][1] \
                    and bi == len(key_list) \
                    or at + duration <= self._pipe[key_list[bi]][0]:
                self._pipe[at] = (at, at + duration, value, easing)
                return True
            else:
                print("Warning: Current action pipe cannot hold this time period: {} - {}".format(at, at + duration))
                return False
        else:
            raise (Exception("ValueError: Unexpected bisection error for time: {}".format(at)))

    def to_list(self):
        """

        :return:
        """
        return list(self._pipe.values())

    def get_latest_value(self, at):
        """
        get the latest state value before query time
        :param at: query time
        :return:
        """
        if at < self._hatch_time or at >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid query time: {}".format(at)))
        key_list = list(self._pipe.keys())
        bi = bisect_right(key_list, at)
        if bi:
            key = key_list[bi-1]
            return self._pipe[key][2]
        else:
            raise (Exception("ValueError: Unexpected bisection error for time: {}".format(at)))


if __name__ == '__main__':
    opacity_pipe = ActionPipe(hatch_time=0, hatch_value=0)
    opacity_pipe.add(at=1, duration=10, value=1, easing="easeInCube")
    opacity_pipe.add(at=20, duration=10, value=0, easing="easeOutCube")
    opacity_pipe.add(at=11, duration=9, value=0.5, easing="linear")
    print(opacity_pipe.to_list())
    print(opacity_pipe.get_latest_value(at=21))

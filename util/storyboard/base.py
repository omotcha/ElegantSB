"""
platform: any
env: any
name: base.py
base classes
"""
from bisect import bisect_right
from configs.config import MAX_PIPE_TIME, TIME_PRECISION


class Vertex:
    """
    Vertex is used for Line Segments, with x,y pos in stageXY coord sys used
    """
    def __init__(self, x, y, z=None):
        self.x = x  # stageX coord sys
        self.y = y  # stageY coord sys
        self.z = 0 if z is None else z  # depth coord sys


class Pos2D:
    """
    Pos2D is a general 2D coord class, by default in noteXY coord sys
    """

    def __init__(self, x, y, coord_sys="note"):
        self.x = x
        self.y = y
        if coord_sys in ["note", "stage", "camera"]:
            self._coord_sys = coord_sys
        else:
            raise (Exception("ParameterError: Invalid coordinate system: {}".format(coord_sys)))

    def get_vertex_by_signature(self):
        """
        :return:
        """
        if self._coord_sys == "stage":
            return Vertex(self.x, self.y)
        else:
            # for test: if a vertex x,y pos supports other coord sys
            return Vertex("{}X:{}".format(self._coord_sys, self.x), "{}Y:{}".format(self._coord_sys, self.y))

    def to_stage_pos(self):
        """
        for test, only support note->stage
        :return:
        """
        if self._coord_sys == "note":
            self.x = round(800*self.x-400, 4)
            self.y = round(600*self.y-300, 4)
            self._coord_sys = "stage"
        else:
            print("Warning: Only note coordinate system can be converted to stage coordinate system.")
        return self

    def to_note_pos(self):
        """
        for test, only support stage->note
        :return:
        """
        if self._coord_sys == "stage":
            self.x = (self.x+400)/800
            self.y = (self.y+300)/600
            self._coord_sys = "note"
        else:
            print("Warning: Only stage coordinate system can be converted to note coordinate system.")
        return self


class Animation:
    def __init__(self):
        self.type = None
        self.mutate_interval = 0.05
        self.easing = "linear"


class NoteFillColors:

    def __init__(self):
        self.up_click = "#FFF"
        self.down_click = "#FFF"
        self.up_drag = "#FFF"
        self.down_drag = "#FFF"
        self.up_hold = "#FFF"
        self.down_hold = "#FFF"
        self.up_long_hold = "#FFF"
        self.down_long_hold = "#FFF"
        self.up_flick = "#FFF"
        self.down_flick = "#FFF"
        self.up_c_drag = "#FFF"
        self.down_c_drag = "#FFF"

    def to_list(self):
        return [self.up_click, self.down_click,
                self.up_drag, self.down_drag,
                self.up_hold, self.down_hold,
                self.up_long_hold, self.down_long_hold,
                self.up_flick, self.down_flick,
                self.up_c_drag, self.down_c_drag]


class NoteSelector:
    def __init__(self):
        self.type = []  # list of acceptable note types
        self.start = None  # start id of note
        self.end = None  # end id of note
        self.direction = None  # 1 for notes scanned upwards, -1 for notes scanned downwards
        self.min_x = None  # minimum x-coord of note
        self.max_x = None  # maximum x-coord of note

    def to_dict(self):
        ret = {
            "type": self.type,
            "start": self.start,
            "end": self.end,
            "direction": self.direction,
            "min_x": self.min_x,
            "max_x": self.max_x
        }
        return ret


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
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            hatch_time = round(hatch_time, TIME_PRECISION)
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
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            at = round(at, TIME_PRECISION)
            duration = round(duration, TIME_PRECISION)
        if at < self._hatch_time or at + duration >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid time period: {} - {}".format(at, at + duration)))
        key_list = list(self._pipe.keys())
        bi = bisect_right(key_list, at)
        if bi:
            if (at >= self._pipe[key_list[bi - 1]][1] and bi == len(key_list)) \
                    or (at >= self._pipe[key_list[bi - 1]][1] and at + duration <= self._pipe[key_list[bi]][0]):
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
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            at = round(at, TIME_PRECISION)
        if at < self._hatch_time or at >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid query time: {}".format(at)))
        key_list = list(self._pipe.keys())
        bi = bisect_right(key_list, at)
        if bi:
            key = key_list[bi-1]
            return self._pipe[key][2]
        else:
            raise (Exception("ValueError: Unexpected bisection error for time: {}".format(at)))


class SwitchPipe:
    """
    [omo]tcha: SwitchPipe is a dictionary to store and manage states of switches.
    Here switch is minimized upon a single property.
    SwitchPipe maintains a dictionary (time:value of property)
    """
    def __init__(self, hatch_time, hatch_value):
        """
        The first action should be "hatch" action
        :param hatch_time:
        :param hatch_value:
        """
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            hatch_time = round(hatch_time, TIME_PRECISION)
        if hatch_time < 0 or hatch_time >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid hatch time: {}".format(hatch_time)))
        self._pipe = {hatch_time: hatch_value}
        self._hatch_time = hatch_time

    def add(self, at, value):
        """
        Add a state to the pipe
        :param at: absolute time
        :param value: value of property
        :return:
        """
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            at = round(at, TIME_PRECISION)
        if at < self._hatch_time or at >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid time: {}".format(at)))
        if at in self._pipe.keys():
            print("Warning: Time already exists in current switch pipe, the value would be overridden by the new one.")
        self._pipe[at] = value

    def to_list(self):
        """

        :return:
        """
        return list(self._pipe.items())

    def get_latest_value(self, at):
        """
        get the latest state value before query time
        :param at: query time
        :return:
        """
        if isinstance(TIME_PRECISION, int) and TIME_PRECISION > 0:
            at = round(at, TIME_PRECISION)
        if at < self._hatch_time or at >= MAX_PIPE_TIME:
            raise (Exception("ValueError: Invalid query time: {}".format(at)))
        key_list = list(self._pipe.keys())
        bi = bisect_right(key_list, at)
        if bi:
            key = key_list[bi-1]
            return self._pipe[key]
        else:
            raise (Exception("ValueError: Unexpected bisection error for time: {}".format(at)))


def get_easing_types():
    easing_directions = ["In", "Out", "InOut"]
    easing_func_types = ["Sine", "Quad", "Cubic", "Quart", "Quint", "Expo", "Circ", "Back", "Elastic", "Bounce"]
    ret = []
    for i in easing_directions:
        for j in easing_func_types:
            ret.append("ease{}{}".format(i, j))
    ret.append("linear")
    return ret


if __name__ == '__main__':
    opacity_pipe = ActionPipe(hatch_time=0, hatch_value=0)
    opacity_pipe.add(at=1, duration=10, value=1, easing="easeInCube")
    opacity_pipe.add(at=20, duration=10, value=0, easing="easeOutCube")
    opacity_pipe.add(at=11, duration=9, value=0.5, easing="linear")

    o_x_pipe = SwitchPipe(hatch_time=0, hatch_value=False)
    o_x_pipe.add(at=1, value=True)
    # print(opacity_pipe.to_list())
    # print(opacity_pipe.get_latest_value(at=21))
    # print(o_x_pipe.to_list())
    # print(o_x_pipe.get_latest_value(at=1.1))
    print(get_easing_types())

"""
platform: any
env: any
name: analyzer.py
json-format chart analyzer
"""
import os
import json
from json.decoder import JSONDecodeError
from configs.config import tmp_dir


class Page:
    def __init__(self, page_dict):
        """
        load page dictionary into pyobj
        :param page_dict: page(dict)
        """
        self.start_tick = page_dict["start_tick"]
        self.end_tick = page_dict["end_tick"]
        self.scan_line_direction = page_dict["scan_line_direction"]


class Tempo:
    def __init__(self, tempo_dict):
        """
        load tempo dictionary into pyobj
        :param tempo_dict: tempo(dict)
        """
        self.tick = tempo_dict["tick"]
        self.value = tempo_dict["value"]


class Note:
    def __init__(self, note_dict):
        """
        load note dictionary into pyobj
        :param note_dict: note(dict)
        """
        self.page_index = note_dict["page_index"]
        self.type = note_dict["type"]
        self.id = note_dict["id"]
        self.tick = note_dict["tick"]
        self.x = note_dict["x"]
        self.has_sibling = note_dict["has_sibling"]
        self.hold_tick = note_dict["hold_tick"]
        self.next_id = note_dict["next_id"]
        self.is_forward = note_dict["is_forward"]


class Events:
    def __init__(self, events_dict):
        """
        load events dictionary into pyobj
        :param events_dict: events(dict)
        """
        self.tick = events_dict["tick"]
        self.event_list = events_dict["event_list"]


class Chart:
    def __init__(self, chart_f):
        """
        load json-format chart's content into a dictionary then into pyobj
        :param chart_f: chart file name(str)
        """
        _, ext = os.path.splitext(chart_f)
        if ext != ".json":
            raise (Exception("Error: Not a valid chart file format: {}".format(ext)))
        try:
            with open(chart_f, "r") as f:
                chart_dict = json.load(f)
        except FileNotFoundError:
            print("Error: No such chart file: {}".format(chart_f))
            return
        except JSONDecodeError:
            print("Error: Bad chart content: {}".format(chart_f))
            return
        self.format_version = chart_dict["format_version"]
        self.time_base = chart_dict["time_base"]
        self.start_offset_time = chart_dict["start_offset_time"]
        self.page_list = []
        self.tempo_list = []
        self.note_list = []
        self.event_order_list = []
        for page in chart_dict["page_list"]:
            self.page_list.append(Page(page))
        for tempo in chart_dict["tempo_list"]:
            self.tempo_list.append(Tempo(tempo))
        # [omo]tcha: add a tail to the tempo list
        self.tempo_list.append(Tempo({"tick": self.get_max_tick(), "value": -1}))
        for note in chart_dict["note_list"]:
            self.note_list.append(Note(note))
        for events in chart_dict["event_order_list"]:
            self.event_order_list.append(Events(events))

        # [omo]tcha: calculate max time
        self.max_time = 0
        for tid in range(len(self.tempo_list)-1):
            self.max_time += (self.tempo_list[tid+1].tick - self.tempo_list[tid].tick) * \
                             self.tempo_list[tid].value / 1000000 / self.time_base

    # callables
    def get_page_num(self):
        return len(self.page_list)

    def get_tempo_num(self):
        # [omo]tcha: tail of the tempo list should not be calculated
        return len(self.tempo_list) - 1

    def get_note_num(self):
        return len(self.note_list)

    def get_events_num(self):
        return len(self.event_order_list)

    def get_max_tick(self):
        return self.page_list[-1].end_tick

    def get_max_time(self):
        return self.max_time

    def test(self):
        pass


# [omo]tcha: chart analyzer toolkit
def get_time(chart_obj, query, by="note_id"):
    """
    calculate absolute time by query
    supported query type: note_id, page_id, tick
    :param chart_obj: chart(Chart)
    :param query: query data
    :param by: query type(str)
    :return: absolute time in seconds
    """
    if not isinstance(chart_obj, Chart):
        print("Error: Invalid input chart")
        return

    if by == "note_id":
        if not isinstance(query, int) or query < 0 or query >= chart_obj.get_note_num():
            print("Error: Invalid note ID: {}".format(query))
            return
        tick = chart_obj.note_list[query].tick

    elif by == "page_id":
        if not isinstance(query, int) or query < 0 or query >= chart_obj.get_page_num():
            print("Error: Invalid page ID: {}".format(query))
            return
        tick = chart_obj.page_list[query].start_tick

    elif by == "tick":
        if not isinstance(query, int) or query < 0 or query > chart_obj.get_max_tick():
            print("Error: Invalid tick value: {}".format(query))
            return
        tick = query

    else:
        print("Error: Not supported query type: {}".format(by))
        return

    abs_time = 0
    cur_tempo_id = 0
    while tick > chart_obj.tempo_list[cur_tempo_id].tick:
        abs_time += (chart_obj.tempo_list[cur_tempo_id + 1].tick - chart_obj.tempo_list[cur_tempo_id].tick) * \
                    chart_obj.tempo_list[cur_tempo_id].value / 1000000 / chart_obj.time_base
        cur_tempo_id += 1
    abs_time -= (chart_obj.tempo_list[cur_tempo_id].tick - tick) * \
                chart_obj.tempo_list[cur_tempo_id - 1].value / 1000000 / chart_obj.time_base
    return abs_time


def get_page_id_by_time(chart_obj, abs_time):
    """
    figure out the page id from absolute time
    :param chart_obj: chart(Chart)
    :param abs_time: absolute time in seconds
    :return: page id(int)
    """
    if not isinstance(chart_obj, Chart):
        print("Error: Invalid input chart")
        return -1

    if abs_time < 0 or abs_time > chart_obj.get_max_time():
        print("Error: Invalid query time: {}".format(abs_time))
        return -1

    page_id = 0
    while page_id < chart_obj.get_page_num() \
            and get_time(chart_obj, chart_obj.page_list[page_id].start_tick, by="tick") <= abs_time:
        page_id += 1
    return page_id - 1


def get_bounding_ticks_by_time(chart_obj, abs_time):
    """
    figure out the bounding ticks from absolute time
    :param chart_obj: chart(Chart)
    :param abs_time: absolute time in seconds
    :return: start_tick(int), end_tick(int)
    """
    page_id = get_page_id_by_time(chart_obj, abs_time)
    if page_id < 0:
        return
    else:
        return chart_obj.page_list[page_id].start_tick, chart_obj.page_list[page_id].end_tick


if __name__ == '__main__':
    chart = Chart(os.path.join(tmp_dir, "chart.json"))
    print(get_time(chart, 728, by="page_id"))
    print(get_bounding_ticks_by_time(chart, 3))

"""
platform: any
env: any
name: chart.py
storyboard and member objects
"""
import os
import json
from json.decoder import JSONDecodeError


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
            raise (Exception("FileError: Not a valid chart file format: {}.".format(ext)))
        try:
            with open(chart_f, "r") as f:
                chart_dict = json.load(f)
        except FileNotFoundError:
            print("FileError: No such chart file: {}.".format(chart_f))
            return
        except JSONDecodeError:
            print("JSONError: Bad chart content: {}.".format(chart_f))
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

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
        :param page_dict:
        """
        self._start_tick = page_dict["start_tick"]
        self._end_tick = page_dict["end_tick"]
        self._scan_line_direction = page_dict["scan_line_direction"]


class Tempo:
    def __init__(self, tempo_dict):
        """
        load tempo dictionary into pyobj
        :param tempo_dict:
        """
        self._tick = tempo_dict["tick"]
        self._value = tempo_dict["value"]


class Note:
    def __init__(self, note_dict):
        """
        load note dictionary into pyobj
        :param note_dict:
        """
        self._page_index = note_dict["page_index"]
        self._type = note_dict["type"]
        self._id = note_dict["id"]
        self._tick = note_dict["tick"]
        self._x = note_dict["x"]
        self._has_sibling = note_dict["has_sibling"]
        self._hold_tick = note_dict["hold_tick"]
        self._next_id = note_dict["next_id"]
        self._is_forward = note_dict["is_forward"]


class Events:
    def __init__(self, events_dict):
        """
        load events dictionary into pyobj
        :param events_dict:
        """
        self._tick = events_dict["tick"]
        self._event_list = events_dict["event_list"]


class Chart:
    def __init__(self, chart_f):
        """
        load json-format chart's content into a dictionary then into pyobj
        :param chart_f:
        """
        _, ext = os.path.splitext(chart_f)
        if ext != ".json":
            raise(Exception("Error: Not a valid chart file format: {}".format(ext)))
        try:
            with open(chart_f, "r") as f:
                chart_dict = json.load(f)
        except FileNotFoundError:
            print("Error: No such chart file: {}".format(chart_f))
            return
        except JSONDecodeError:
            print("Error: Bad chart content: {}".format(chart_f))
            return
        self._format_version = chart_dict["format_version"]
        self._time_base = chart_dict["time_base"]
        self._start_offset_time = chart_dict["start_offset_time"]
        self._page_list = []
        self._tempo_list = []
        self._note_list = []
        self._event_order_list = []
        for page in chart_dict["page_list"]:
            self._page_list.append(Page(page))
        for tempo in chart_dict["tempo_list"]:
            self._tempo_list.append(Tempo(tempo))
        for note in chart_dict["note_list"]:
            self._note_list.append(Note(note))
        for events in chart_dict["event_order_list"]:
            self._event_order_list.append(Events(events))

    # callables
    def test(self):
        pass


if __name__ == '__main__':
    chart = Chart(os.path.join(tmp_dir, "chart.json"))
    chart.test()

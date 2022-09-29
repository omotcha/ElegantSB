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
        self.start_tick = page_dict["start_tick"]
        self.end_tick = page_dict["end_tick"]
        self.scan_line_direction = page_dict["scan_line_direction"]


class Tempo:
    def __init__(self, tempo_dict):
        """
        load tempo dictionary into pyobj
        :param tempo_dict:
        """
        self.tick = tempo_dict["tick"]
        self.value = tempo_dict["value"]


class Note:
    def __init__(self, note_dict):
        """
        load note dictionary into pyobj
        :param note_dict:
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
        :param events_dict:
        """
        self.tick = events_dict["tick"]
        self.event_list = events_dict["event_list"]


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
        # add a tail to the tempo list
        self.tempo_list.append(Tempo({"tick": self.get_max_tick(), "value": -1}))
        for note in chart_dict["note_list"]:
            self.note_list.append(Note(note))
        for events in chart_dict["event_order_list"]:
            self.event_order_list.append(Events(events))

    # callables
    def get_page_num(self):
        return len(self.page_list)

    def get_tempo_num(self):
        # [omo]tcha: tail of the tempo list should not be calculated
        return len(self.tempo_list)-1

    def get_note_num(self):
        return len(self.note_list)

    def get_events_num(self):
        return len(self.event_order_list)

    def get_max_tick(self):
        return self.page_list[-1].end_tick

    def test(self):
        pass


# [omo]tcha: chart analyzer toolkit
def get_time(chart_obj, query, by="note_id"):
    """
    calculate absolute time by query
    supported item to be converted: note_id, tick
    :param chart_obj: Chart(pyobj)
    :param query:
    :param by:
    :return:
    """
    if not isinstance(chart_obj, Chart):
        print("Error: Invalid input chart")
        return
    if by == "note_id":
        if not isinstance(query, int) or query < 0 or query >= chart_obj.get_note_num():
            print("Error: Invalid note ID")
            return
        tick = chart_obj.note_list[query].tick

        abs_time = 0
        cur_tempo_id = 0
        while tick > chart_obj.tempo_list[cur_tempo_id].tick:
            abs_time += (chart_obj.tempo_list[cur_tempo_id+1].tick - chart_obj.tempo_list[cur_tempo_id].tick) * \
                        chart_obj.tempo_list[cur_tempo_id].value / 1000000 / chart_obj.time_base
            cur_tempo_id += 1
        abs_time -= (chart_obj.tempo_list[cur_tempo_id].tick - tick) * \
                    chart_obj.tempo_list[cur_tempo_id-1].value / 1000000 / chart_obj.time_base
        return abs_time
    elif by == "tick":
        if not isinstance(query, int) or query < 0 or query > chart_obj.get_max_tick():
            print("Error: Invalid tick value")
            return

        abs_time = 0
        cur_tempo_id = 0
        while query > chart_obj.tempo_list[cur_tempo_id].tick:
            abs_time += (chart_obj.tempo_list[cur_tempo_id + 1].tick - chart_obj.tempo_list[cur_tempo_id].tick) * \
                        chart_obj.tempo_list[cur_tempo_id].value / 1000000 / chart_obj.time_base
            cur_tempo_id += 1
        abs_time -= (chart_obj.tempo_list[cur_tempo_id].tick - query) * \
                    chart_obj.tempo_list[cur_tempo_id - 1].value / 1000000 / chart_obj.time_base
        return abs_time
    else:
        print("Error: Not supported item type")
        return


if __name__ == '__main__':
    chart = Chart(os.path.join(tmp_dir, "chart.json"))
    print(get_time(chart, 0, by="note_id"))
    print(get_time(chart, 650000, by="tick"))

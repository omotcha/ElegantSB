"""
platform: any
env: any
name: analyzer.py
chart analyzer toolkit
"""
import os
from util.chart.chart import Chart
from configs.config import example_dir


class ChartAnalyzer:

    def __init__(self, chart_f):
        self._chart = Chart(chart_f)

    def get_time(self, query, by="note_id"):
        """
        calculate absolute time by query
        supported query type: note_id, page_id, tick
        :param query: query data
        :param by: query type(str)
        :return: absolute time in seconds
        """
        if by == "note_id":
            if not isinstance(query, int) or query < 0 or query >= self._chart.get_note_num():
                print("QueryError: Invalid note ID: {}.".format(query))
                return
            tick = self._chart.note_list[query].tick

        elif by == "page_id":
            if not isinstance(query, int) or query < 0 or query >= self._chart.get_page_num():
                print("QueryError: Invalid page ID: {}.".format(query))
                return
            tick = self._chart.page_list[query].start_tick

        elif by == "tick":
            if not isinstance(query, int) or query < 0 or query > self._chart.get_max_tick():
                print("QueryError: Invalid tick value: {}.".format(query))
                return
            tick = query

        else:
            print("QueryError: Not supported query type: {}.".format(by))
            return

        abs_time = 0
        cur_tempo_id = 0
        while tick > self._chart.tempo_list[cur_tempo_id].tick:
            abs_time += (self._chart.tempo_list[cur_tempo_id + 1].tick - self._chart.tempo_list[cur_tempo_id].tick) * \
                        self._chart.tempo_list[cur_tempo_id].value / 1000000 / self._chart.time_base
            cur_tempo_id += 1
        abs_time -= (self._chart.tempo_list[cur_tempo_id].tick - tick) * \
                    self._chart.tempo_list[cur_tempo_id - 1].value / 1000000 / self._chart.time_base
        return abs_time

    def get_page_id_by_time(self, abs_time):
        """
        figure out the page id from absolute time
        :param abs_time: absolute time in seconds
        :return: page id(int)
        """
        if abs_time < 0 or abs_time > self._chart.get_max_time():
            print("QueryError: Invalid query time: {}.".format(abs_time))
            return -1

        page_id = 0
        while page_id < self._chart.get_page_num() \
                and self.get_time(self._chart.page_list[page_id].start_tick, by="tick") <= abs_time:
            page_id += 1
        return page_id - 1

    def get_bounding_ticks_by_time(self, abs_time):
        """
        figure out the bounding ticks from absolute time
        :param abs_time: absolute time in seconds
        :return: start_tick(int), end_tick(int)
        """
        page_id = self.get_page_id_by_time(abs_time)
        if page_id < 0:
            return
        else:
            return self._chart.page_list[page_id].start_tick, self._chart.page_list[page_id].end_tick


if __name__ == '__main__':
    analyzer = ChartAnalyzer(os.path.join(example_dir, "nhelv.json"))
    print(analyzer.get_time(100, by="page_id"))
    print(analyzer.get_bounding_ticks_by_time(3))

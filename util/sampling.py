"""
platform: any
env: any
name: Sampling.py
Key time and key position generator util
"""
import math
from util.storyboard.base import Pos2D


class Pos2DSampler:
    """
    Pos2DSampler is a 2D point sampler based on a polar coord sys.
    It can be directly converted to noteXY coord sys.
    """

    def __init__(self, n_sample):
        """
        create a list of Pos2D objects
        :param n_sample: number of samples
        """
        if n_sample <= 0 or not isinstance(n_sample, int):
            raise (Exception("ParameterError: Invalid number of samples: {}.".format(n_sample)))
        self._samples = []
        for i in range(n_sample):
            self._samples.append(Pos2D(0, 0))
        self._sample_types = ["circle"]

    @staticmethod
    def _circle(r, t, a=0.5, b=0.5):
        """
        the parametric equation of a circle
        :param r: radius
        :param t: theta, in degree
        :param a: center x-coord in cartesian coord sys
        :param b: center y-coord in cartesian coord sys
        :return:
        """
        t = math.radians(t)
        x = round(a * r * math.cos(t) + b, 4)
        y = round(a * r * math.sin(t) + b, 4)
        return x, y

    # [omo]tcha: callables
    def get_samples(self):
        return self._samples

    def sample(self, sample_type=None, option=None):
        """

        :param sample_type:
        :param option:
        :return:
        """
        if sample_type in self._sample_types:
            pass
        else:
            raise (Exception("ParameterError: Invalid sampling type: {}".format(sample_type)))

        ret = []
        if sample_type == "circle":
            if option is None:
                option = 0
            deg_list = uniform_time_segment(option, option+360, n_seg=len(self._samples))

            for i in range(len(deg_list) - 1):
                x, y = self._circle(1, deg_list[i])
                ret.append(Pos2D(x, y, coord_sys="note"))
        return ret


def uniform_time_segment(start, end, n_seg):
    """

    :param start: start time (absolute time)
    :param end: end time (absolute time)
    :param n_seg: number of time segments
    :return:
    """
    if n_seg < 0 or not isinstance(n_seg, int):
        raise (Exception("ParameterError: Invalid number of segments: {}.".format(n_seg)))
    if start > end:
        raise (Exception("LogicError: Start time should be smaller than end time."))

    seg = (end-start)/n_seg
    return [round(start+i*seg, 3) for i in range(n_seg+1)]


if __name__ == '__main__':
    print(uniform_time_segment(0, 360, 4))

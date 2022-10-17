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
    Pos2DSampler is a 2D point sampler based on a cartesian/polar coord sys.
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
        self._sample_types = ["circle", "line"]

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
                # [omo]tcha: here option is the degree of the first sampling point
                option = 0.0
            if not isinstance(option, int) and not isinstance(option, float):
                raise (Exception("FormatError: Invalid value for degree: {}".format(option)))
            deg_list = uniform_segment(option, option+360, n_seg=len(self._samples))
            for i in range(len(deg_list) - 1):
                x, y = self._circle(1, deg_list[i])
                ret.append(Pos2D(x, y, coord_sys="note"))
        elif sample_type == "line":
            if not isinstance(option, tuple):
                # [omo]tcha: here option is (x1,y1,x2,y2) indicating two end points of a line segment
                raise (Exception("FormatError: Invalid value for end points: {}".format(option)))
            if len(option) != 4 or (option[0] == option[2] and option[1] == option[3]):
                raise (Exception("FormatError: Invalid value for end points: {}".format(option)))
            for i in range(4):
                if option[i] < 0 or option[i] > 1:
                    raise (Exception("FormatError: Invalid value for end points: {}".format(option)))
            x = uniform_segment(option[0], option[2], n_seg=len(self._samples)-1)
            y = uniform_segment(option[1], option[3], n_seg=len(self._samples)-1)
            for i in range(len(self._samples)):
                ret.append(Pos2D(x[i], y[i], coord_sys="note"))

        return ret


def uniform_segment(start, end, n_seg):
    """
    cut a segment(e.g. time period)into smaller pieces in a uniform way
    :param start: start value
    :param end: end value
    :param n_seg: number of segments
    :return:
    """
    if n_seg < 0 or not isinstance(n_seg, int):
        raise (Exception("ParameterError: Invalid number of segments: {}.".format(n_seg)))
    if start > end:
        raise (Exception("LogicError: Start time should be smaller than end time."))

    seg = (end-start)/n_seg
    return [round(start+i*seg, 3) for i in range(n_seg+1)]


if __name__ == '__main__':
    print(uniform_segment(0, 360, 4))

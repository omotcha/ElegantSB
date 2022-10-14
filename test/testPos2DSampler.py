"""
platform: any
env: any
name: testPos2DSampler.py
Pos2DSampler tester
"""

from util.sampling import Pos2DSampler


def test():
    sampler = Pos2DSampler(n_sample=20)
    samples = sampler.sample(sample_type="circle")
    for i in samples:
        print(i.x, i.y)


if __name__ == '__main__':
    test()

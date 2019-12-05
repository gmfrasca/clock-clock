from clockclock.fullclock import FullClock
import argparse

DEFAULT_SNAPPING_FACTOR = 3

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clockwise_only", action="store_true")
    parser.add_argument("-r", "--rotate_on_same", action="store_true")
    parser.add_argument("-s", "--snapping_factor",
                       type=int, default=DEFAULT_SNAPPING_FACTOR)
    return parser.parse_args()

def main():
    args = parse_args()
    fc = FullClock(args.clockwise_only, args.rotate_on_same, args.snapping_factor)
    fc.run()

if __name__ == '__main__':
    main()

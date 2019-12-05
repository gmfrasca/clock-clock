from clockclock.fullclock import FullClock
import argparse


DEFAULT_SNAPPING_FACTOR = 3
DEFAULT_UPDATE_TIME = 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--clockwise_only", action="store_true")
    parser.add_argument("-r", "--rotate_on_same", action="store_true")
    parser.add_argument("-s", "--snapping_factor", type=float,
                        default=DEFAULT_SNAPPING_FACTOR)
    parser.add_argument("-u", "--update_time", type=int,
                        default=DEFAULT_UPDATE_TIME)
    return parser.parse_args()


def main():
    args = parse_args()
    fc = FullClock(args.clockwise_only, args.rotate_on_same,
                   args.snapping_factor, args.update_time)
    fc.run()


if __name__ == '__main__':
    main()

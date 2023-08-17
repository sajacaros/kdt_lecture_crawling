import os

import cell_merge
import kdt

schedule_tough = 'lecture_t.xlsx'
schedule_fine = 'lecture.xlsx'


def main():
    remove_file(schedule_tough)
    remove_file(schedule_fine)

    kdt.start_crawling(schedule_tough)
    cell_merge.merge_same_value(from_source=schedule_tough, to_source=schedule_fine)
    if schedule_tough != schedule_fine:
        remove_file(schedule_tough)


def remove_file(f):
    try:
        os.remove(f)
        print(f"{f} - remove")
    except FileNotFoundError:
        print(f"{f} - already removed")


if __name__ == '__main__':
    main()

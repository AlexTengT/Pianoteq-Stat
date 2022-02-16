#
# This script will show you how long you have played in pianoteq.
# this script should be placed in the under /Archive. (The same path as 20xx folder)
# v3.1
# Alex Teng © 2022

import os
from pathlib import Path
import datetime
import sys

date_of_today = datetime.datetime.today()


# For the given path, get the List of all files in the directory tree
def get_list_of_files(dirName):
    # create a list of file and sub directories
    # names in the given directory
    list_of_file = os.listdir(dirName)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_file:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            all_files = all_files + get_list_of_files(fullPath)
        else:
            all_files.append(fullPath)

    return all_files


# return how long you played (in secs) of tehe given day
# [_dt, _day_of_week, _count_note, _duration[0]]
def get_detail_of_the_day(_dt: list, _given_date: datetime.datetime):
    _dur = 0
    _notes = 0
    for i in _dt:
        if i[0].date() == _given_date.date():
            _dur += i[3]
            _notes += i[2]
    return _dur, _notes


# clean the file names (only filename, without path)
def get_clean_file_name_list():
    targetPath = "Archive/"
    base_path = Path(__file__).parent
    file_path = (base_path / targetPath).resolve()
    file_name_list = get_list_of_files(file_path)

    clean_file_name_list = []

    # build the clean_file_name_list (only filename, without path)
    for i in file_name_list:
        clean_item_name = os.path.basename(i)
        if clean_item_name in [".DS_Store"]:
            continue

        clean_item_name = clean_item_name.split(",")
        part1 = clean_item_name[0].split(" ")
        part2 = clean_item_name[1]

        _date = part1[0]  # the date
        _time = int(part1[1])
        _time_hour = part1[1][:2]
        _time_min = part1[1][2:]

        _dt = _date + " " + _time_hour + " " + _time_min
        _dt = datetime.datetime.strptime(_dt, '%Y-%m-%d %H %M')

        _day_of_week = part1[2][1:-1]
        _count_note = int(part1[3])  # the number of note played
        _duration = [int(s) for s in part2.split() if s.isdigit()]  # in sec

        # print(_dt)
        # print(_date)
        # print(_time)
        # print(_time_hour)
        # print(_time_min)
        # print(day_of_week)
        # print(count_note)
        # print(duration[0])

        clean_file_name_list.append([_dt, _day_of_week, _count_note, _duration[0]])

    return clean_file_name_list


def generate_total_report(_clean_file_name_list):
    # total time
    total_in_sec = 0
    for i in _clean_file_name_list:
        total_in_sec += i[3]

    total_in_min = round(total_in_sec / 60, 2)
    total_in_hour = round(total_in_min / 60, 2)
    total_in_day = round(total_in_hour / 24, 2)
    print("Total：")
    print("     You have played for " + str(total_in_sec) + " secs, ")
    print("     that is " + str(total_in_min) + " mins, ")
    print("     that is " + str(total_in_hour) + " hours, ")
    print("     that is " + str(total_in_day) + " days. ")
    print()
    # total notes
    total_notes = 0
    for i in _clean_file_name_list:
        total_notes += i[2]
    print("     You have played " + str(total_notes) + " notes, totally")


def generate_report_by_day(_clean_file_name_list, _date: datetime.datetime):
    _report = get_detail_of_the_day(_clean_file_name_list, _date)
    _notes = _report[1]
    _in_sec = _report[0]
    _in_min = round(_in_sec / 60, 2)
    _in_hour = round(_in_min / 60, 2)
    print(str(_date.date().strftime("%Y-%m-%d")))
    print("     You have played for " + str(_in_sec) + " secs, ")
    print("     that is " + str(_in_min) + " mins, ")
    print("     that is " + str(_in_hour) + " hours, ")
    print()
    print("     You have played " + str(_notes) + " notes, Today")


# generate_general_report()
def generate_general_report(_clean_file_name_list):
    print()
    generate_total_report(_clean_file_name_list)
    print()
    generate_report_by_day(_clean_file_name_list)


def generate_beginning():
    print("########################################################")
    print("------ Piano Playing Report (" + date_of_today.strftime("%Y-%m-%d %H:%m") + ")------")


def generate_ending():
    print("########################################################")

def generate_help():
    print("""Help on pianoteq-stat.py
Usage: Python3 Howlong.py [arg1] [arg2]
Argument:
  report(default): get general report
  today: get report of today
  yesterday: get report of yesterday
  date 2022-02-06: get report of specific day
  help: get help
  (on dev)thisweek: get report of this week
  (on dev)achievement: get the achievement (toppest)
    """)

def main(args):
    clean_file_name_list = get_clean_file_name_list()

    if args[1] == 'today':
        generate_beginning()
        generate_report_by_day(clean_file_name_list, datetime.datetime.today())
        generate_ending()
    elif args[1] == 'yesterday':
        yesterday = date_of_today - datetime.timedelta(days=1)
        generate_beginning()
        generate_report_by_day(clean_file_name_list, yesterday)
        generate_ending()
    elif args[1] == 'report':
        generate_beginning()
        generate_total_report(clean_file_name_list)
        print()
        generate_report_by_day(clean_file_name_list, datetime.datetime.today())
        generate_ending()

    elif args[1] == 'date':
        _d = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        generate_beginning()
        generate_report_by_day(clean_file_name_list, _d)
        generate_ending()

    elif args[1] == 'help':
        generate_help()

    else:
        print("Your arguments is not correct!")



# Help on pianoteq-stat.py
# Usage: Python3 Howlong.py [arg1] [arg2]
# Argument:
#   report(default): get general report
#   today: get report of today
#   yesterday: get report of yesterday
#   date 2022-02-06: get report of specific day
#   help: get help
#   (on dev)thisweek: get report of this week
#   (on dev)achievement: get the achievement (toppest)

if __name__ == "__main__":
    args = sys.argv
    if len(sys.argv) == 1:
        args.append('report')

    main(args)

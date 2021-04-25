#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta

if len(sys.argv) > 2 or any(map(lambda a: a in ('-h', '--help'), sys.argv)):
    print(f'Usage: {sys.argv[0]} [FILE_LENGTH] <chapters')
    print('Expects chapter list formatted like "HH:MM:SS;Chapter name" on stdin, one chapter per line.')
    print('e.g. "00:00:00;Chapter 1 ')
    print('      00:45:13;Chapter 2 ')
    print('      01:03:00;Chapter 3"')
    print('If no file length specified as argument, last chapter will not have END= attribute')
    print('FILE_LENGTH has HH:MM:SS format, just like the chapters.')
    exit(0)

prev_title = None
def push_end(delta):
    if prev_title:
        if delta:
            print(f'END={delta}')
        print(f'title={prev_title}')
def parse_dur(time):
    t = datetime.strptime(time,"%H:%M:%S")
    delta_s = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta_s.seconds * 1000
for lraw in sys.stdin:
    time, name = lraw.rstrip('\r\n').split(';')
    delta = parse_dur(time)
    push_end(delta)
    print('[CHAPTER]')
    print('TIMEBASE=1/1000')
    print(f'START={delta}')
    prev_title = name
if len(sys.argv) < 2:
    flen = None
else:
    flen = parse_dur(sys.argv[1])
push_end(flen)

#!/usr/bin/env python3

import sys
from datetime import datetime, timedelta


prev_title = None
last_offset = None

def warn(s):
    sys.stderr.write(f'WARN: {s}\n')

def push_end(delta):
    if prev_title is None:
        return
    if delta is not None:
        print(f'END={delta}')
    print(f'title={prev_title}')

def parse_dur(time):
    t = datetime.strptime(time,"%H:%M:%S")
    delta_s = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta_s.seconds * 1000

def routine():
    global last_offset, prev_title

    if len(sys.argv) > 2 or any(map(lambda a: a in ('-h', '--help'), sys.argv)):
        print(f'Usage: {sys.argv[0]} [FILE_LENGTH] <chapters')
        print('Expects chapter list formatted like "HH:MM:SS;Chapter name" on stdin, one chapter per line.')
        print('Leading zeroes can be omitted.')
        print('e.g. "00:00:00;Chapter 1 ')
        print('      00:45:13;Chapter 2 ')
        print('      01:03:00;Chapter 3"')
        print('If no file length specified as argument, last chapter will not have END= attribute')
        print('FILE_LENGTH has HH:MM:SS format, just like the chapters.')
        exit(0)

    for lraw in sys.stdin:
        time, name = lraw.rstrip('\r\n').split(';', 1)
        delta = parse_dur(time)

        if last_offset is not None and delta < last_offset:
            warn(f'Chapter has gone backwards ({delta} < {last_offset}, "{name}")')

        push_end(delta)
        print('[CHAPTER]')
        print('TIMEBASE=1/1000')
        print(f'START={delta}')
        prev_title = name
        last_offset = delta

    if len(sys.argv) < 2:
        flen = None
    else:
        flen = parse_dur(sys.argv[1])
        if last_offset is not None and flen < last_offset:
            warn(f'File length is before last chapter`s START ({flen} < {last_offset})')
    push_end(flen)

if __name__ == '__main__':
    routine()


#!/usr/bin/python

# Michael Nugent
# michael (at symbol) michaelnugent - org
# GPL-v2

import sys,re
import mmap
from struct import unpack

def check_magic(magic):
    if magic == "<magic here>":
        return True
    else:
        return False

def decode_header(map, offset):
    header = {}
    header['timestamp'] = unpack('i', map[offset+0:offset+4])[0]
    #print "timestamp", header['timestamp']
    header['type_code'] = unpack('b', map[offset+4])[0]
    header['server_id'] = unpack('i', map[offset+5:offset+9])[0]
    header['event_length'] = unpack('i', map[offset+9:offset+13])[0]
    header['next_position'] = unpack('i', map[offset+13:offset+17])[0]
    #print "next_position", header['next_position']
    header['flags'] = unpack('h', map[offset+17:offset+19])[0]
    header['binlog_version'] = unpack('h', map[offset+19:offset+21])[0]
    header['server_version'] = map[offset+21:offset+71][0]
    header['create_timestamp'] = unpack('i', map[offset+71:offset+75])[0]
    header['header_length'] = unpack('b', map[offset+75:offset+76])[0]
    return header

def event_format_desc(header, map, offset):
    data_length = header['event_length'] - header['header_length']
    data_start = offset+header['header_length']
    data_end = data_start + data_length
    #print unpack('h', map[data_start:data_start+2])[0]
    #print map[data_start+2:data_start+52]
    #print unpack('i', map[data_start+52:data_start+56])[0]
    #print unpack('b', map[data_start+56:data_start+57])[0]
    return header['next_position']

def event_write_rows(header, map, offset):
    return header['next_position']

def event_update_rows(header, map, offset):
    print map[offset:offset+6]
    print unpack('h', map[offset+8:offset+10])
    return header['next_position']

def event_delete_rows(header, map, offset):
    return header['next_position']

def event_table_map(header, map, offset):
    return header['next_position']

def event_pass(header, map, offset):
    return header['next_position']

events = { 
            2: event_pass,
            15: event_format_desc,
            19: event_table_map,
            23: event_write_rows,
            24: event_update_rows,
            25: event_delete_rows,
         }


f = open(sys.argv[1], 'r+')
map = mmap.mmap(f.fileno(), 0)
size = map.size()
print "total size", size

offset = 4
check_magic(unpack('i', map[0:4]))

while True:
    header = decode_header(map, offset)
    #print "type_code", header['type_code']
    #print "offset before", offset
    offset = events[header['type_code']](header, map, offset)
    #print "offset after", offset
    #print "next_position", header['next_position']
    if header['next_position'] + 19 >= size:
        break
    #offset = offset + offset_change - 4
    #print "s----"
    #print offset
    #print "e----"

map.close()
f.close()



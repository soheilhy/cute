#!/usr/bin/python
# Copyright 2011 HiPerNet Research Group, University of Toronto. All Rights
# Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

__author__ = 'Soheil Hassas Yeganeh <soheil@cs.toronto.edu>'

ESCAPE_TOKEN = '// ESCAPED //'

def extract_payload_and_label_from_csv(csv_path, payload_start_index,
    payload_end_index, protocol_index, delimiter='|', escape_char='\\',
    flow_per_protocol=1000):
  """ Extracts the payload and label from a csv for futher processing. """
  escape_str = escape_char + delimiter
  protocol_to_flow_map = {}

  for line in open(csv_path):
    line_splitted = line.replace(escape_str, ESCAPE_TOKEN)\
        .split(delimiter)
    protocol = line_splitted[protocol_index]
    flow_list = protocol_to_flow_map.get(protocol)
    if not flow_list:
      flow_list = []
      protocol_to_flow_map[protocol] = flow_list
    elif len(flow_list) >= flow_per_protocol:
      continue
    payload = delimiter.join(
        line_splitted[payload_start_index:payload_end_index])\
        .replace(ESCAPE_TOKEN, escape_str)
    flow_list.append(payload)

  return protocol_to_flow_map

def serialize_dataset(dataset):
  for protocol, flows in dataset.iteritems():
    print protocol, ':'
    for flow in flows:
      print flow

def print_usage():
  print ('USAGE: utils.py -f <payload_start_index> -t <payload_end_index>'
      '-p <protocol> [-d <delimiter>] [-e <escape_char>]'
      '[-n <flows_per_protocol>] <csv_file>')

if __name__ == '__main__':
  import getopt
  import sys

  if len(sys.argv) < 7:
    print_usage()
    sys.exit(-1)

  opts, args = getopt.getopt(sys.argv, 'ftpd:e:n:')
  dataset = extract_payload_and_label_from_csv(csv_path=args[1],
      payload_start_index=opts['f'], payload_end_index=opts['t'],
      protocol_index=opts['p'])

  serialize_dataset(dataset)

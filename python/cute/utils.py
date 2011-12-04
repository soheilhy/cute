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

import re

ESCAPE_TOKEN = '// ESCAPED //'

def extract_payload_and_label_from_csv(csv_path, payload_start_index,
    payload_end_index, protocol_index, aggregator_index=None,
    accept_numerical_payload=False, delimiter='|', escape_char='\\',
    flow_per_protocol=1000):
  """ Extracts the payload and label from a csv for futher processing. """
  escape_str = escape_char + delimiter
  protocol_to_flow_map = {}

  prev_aggregator = None
  prev_protocol = None
  for line in open(csv_path, encoding='ascii', errors='ignore'):
    line_splitted = line.replace(escape_str, ESCAPE_TOKEN)\
        .split(delimiter)
    if len(line_splitted) <= max(payload_end_index, protocol_index):
      continue
    protocol = line_splitted[protocol_index]
    flow_list = protocol_to_flow_map.get(protocol)
    if not flow_list:
      flow_list = []
      protocol_to_flow_map[protocol] = flow_list
    elif len(flow_list) >= flow_per_protocol:
      continue

    prefix = ''
    if aggregator_index:
      aggregator = line_splitted[aggregator_index]
      if aggregator == prev_aggregator and prev_protocol == protocol:
        prefix = flow_list.pop()
      else:
        prev_aggregator = aggregator
        prev_protocol = protocol
    payload_parts = line_splitted[payload_start_index:payload_end_index]
    for part in payload_parts:
      if accept_numerical_payload or not re.match('^\\d*$', part):
        prefix += delimiter + part
    payload = prefix.replace(ESCAPE_TOKEN, escape_str)

    flow_list.append(payload)

  return protocol_to_flow_map

def serialize_dataset(dataset):
  for protocol, flows in dataset.items():
    for flow in flows:
      print(protocol + '|' + flow)

def load_dataset(path, separator='|'):
  dataset = []
  for line in open(path, encoding='ascii', errors='ignore'):
    seperator_index = line.find(separator)
    if seperator_index != -1:
      protocol = line[0:seperator_index]
      payload = line[seperator_index+1:]
      dataset += [(payload, protocol)]
  return dataset

def print_usage():
  print('USAGE: utils.py -f <payload_start_index> -t <payload_end_index>'
      '-p <protocol> [-d <delimiter>] [-e <escape_char>]'
      '[-n <flows_per_protocol>] <csv_file>')

if __name__ == '__main__':
  import getopt
  import sys

  if len(sys.argv) < 7:
    print_usage()
    sys.exit(-1)


  payload_end_index = payload_start_index = protocol_index = aggregator_index =\
      -1
  accept_numerical_payload = False
  opts, args = getopt.getopt(sys.argv[1:], 'f:t:p:a:d:e:n:x')
  for opt, value in opts:
    if opt == '-f':
      payload_start_index = int(value)
    elif opt == '-t':
      payload_end_index = int(value)
    elif opt == '-p':
      protocol_index = int(value)
    elif opt == '-a':
      aggregator_index = int(value)
    elif opt == '-x':
      accept_numerical_payload = True

  dataset = extract_payload_and_label_from_csv(args[0],
      payload_start_index, payload_end_index,
      protocol_index, aggregator_index, accept_numerical_payload)

  serialize_dataset(dataset)

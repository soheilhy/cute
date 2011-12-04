#!/usr/bin/python3
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

import getopt
import sys

import utils

class StringUtils(object):
  def extract_all_common_terms(str1, str2, length_threshold=4,
      cache=None):
    str_len1 = len(str1)
    str_len2 = len(str2)
    if min(str_len1, str_len2) < length_threshold:
      return []

    if not str1 or not str2:
      return []

    cache_key = StringUtils._hash_string_tuple(str1, str2, length_threshold)
    if cache != None:
      cached_substrings = cache.get(cache_key)
      if cached_substrings != None:
        return cached_substrings

    all_substrings = []
    current_term = ''
    current_term_len = 0
    for i in range(str_len1):
      for j in range(str_len2):
        for k in range(min(str_len1 - i, str_len2 - j)):
          if str1[i + k] == str2[j + k]:
            current_term += str1[i + k]
            current_term_len += 1
          else:
            if current_term_len >= length_threshold:
              for i in range(length_threshold, current_term_len + 1):
                all_substrings += StringUtils._all_permutations(current_term, i)
            current_term = ''
            current_term_len = 0
            break

    if cache != None:
      cache[cache_key] = all_substrings

    return sorted(set(all_substrings))

  def _hash_string_tuple(str1, str2, length_threshold):
    sorted_strings = sorted([str1, str2])
    return '%s&%s&%d' % (sorted_strings[0], sorted_strings[1], length_threshold)

  def _all_permutations(term, length_threshold):
    return [term[i:i+length_threshold]
        for i in range(0, len(term) - length_threshold + 1)]

  def match_text_with_terms(text, terms):
    return [term for term in terms if text.find(term) != -1]

class TermFrequencyUtils(object):
  def find_common_term_frequencies(data_set, payload_max_length=50,
      length_threshold=4):
    term_cache = {}
    term_frequencies = {} # A dict from term->protocol->frequency
    protocol_counts = {}
    dataset_len = len(data_set)
    for i in range(dataset_len):
      print(i, end='\r', file=sys.stderr)
      common_terms = []
      payload1, protocol1 = data_set[i]
      payload1 = payload1[0:payload_max_length]
      protocol_count = protocol_counts.get(protocol1)
      if protocol_count == None:
        protocol_count = 0
      protocol_counts[protocol1] = protocol_count + 1

      for j in range(dataset_len):
        if i == j:
          continue
        payload2, protocol2 = data_set[j]
        payload2 = payload2[0:payload_max_length]
        common_terms += StringUtils.extract_all_common_terms(payload1, payload2,
            length_threshold, term_cache)

      for term in set(common_terms):
        protocol_frequencies = term_frequencies.get(term)
        if protocol_frequencies == None:
          protocol_frequencies = {}
          term_frequencies[term] = protocol_frequencies

        frequency1 = protocol_frequencies.get(protocol1)
        protocol_frequencies[protocol1] =\
            frequency1 + 1 if frequency1 != None else 1

    for term, protocol_frequencies in term_frequencies.items():
      for protocol, freq in protocol_frequencies.items():
        protocol_frequencies[protocol] = freq / protocol_counts[protocol]

    return term_frequencies

  def serialize_term_frequencies(term_frequencies, separator='|'):
    for term, protocol_frequencies in term_frequencies.items():
      for protocol, freq in protocol_frequencies.items():
        print(separator.join([protocol, str(freq), term]))

  def prune_terms(path):
    lines = [line[:-1] for line in open(path)]
    i = 0
    for line in lines:
      print(i+=1, end='\r', file=sys.stderr)
      should_be_prune = False
      protocol, frequency, term = TermFrequencyUtils._parse_term_line(line)
      if not term:
        continue
      for line2 in lines:
        if line == line2:
          continue
        protocol2, frequency2, term2 = TermFrequencyUtils._parse_term_line(
            line2)
        if not term2:
          continue
        if term2.find(term) != -1 and protocol2 == protocol and\
            frequency2 >= frequency:
          should_be_prune = True
          break
      if not should_be_prune:
        print(line)

  def _parse_term_line(line, separator='|'):
    protocol_end = line.find(separator)
    frequency_end = line.find(separator, protocol_end + 1)
    if frequency_end == -1 or protocol_end == -1:
      return (None, None, None)
    term = line[frequency_end + 1:]
    frequency = float(line[protocol_end + 1: frequency_end])
    protocol = line[:protocol_end]
    return (protocol, frequency, term)

def print_usage():
  print('USAGE: terms.py -t separator -l length_threshold -p payload_length'
        'dataset_path')

if __name__ == '__main__':
  opts, args = getopt.getopt(sys.argv[1:], 't:l:p:x')
  if len(args) == 0:
    print_usage()
    sys.exit(-1)

  separator = '|'
  length_threshold = 4
  payload_max_length = 50
  prune = False

  for opt, value in opts:
    if opt == '-t':
      separator = value
    elif opt == '-l':
      length_threshold = int(value)
    elif opt == '-p':
      payload_max_length = int(value)
    elif opt == '-x':
      prune = True

  if prune:
    TermFrequencyUtils.prune_terms(args[0])
  else:
    dataset = utils.load_dataset(args[0])
    tf = TermFrequencyUtils.find_common_term_frequencies(
        dataset, payload_max_length, length_threshold)
    TermFrequencyUtils.serialize_term_frequencies(tf)


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

import abc
import cute.weight

class Classifier(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def classify(self, payload):
    """ Classifies the payload.

    Args:
      payload: The application layer flow payload.

    Returns:
      The list of protocols.
    """
    return

class Cute(Classifier):

  def __init__(self, weighted_terms):
    self._weighted_terms = weighted_terms

  def classify(self, payload):
    """Classifies the payload according the given set of weighted terms.

    Note that payload should be headerless.

    Args:
      payload: The application layer flow payload.

    Returns:
      The list of detected protocols. Empty list returned if unable to classify.
    """
    if not payload:
      return []

    max_similarity = -1
    best_protocols = []
    for protocol, list_of_terms in self._weighted_terms.iteritems():
      sum_of_weights = 0
      matched_term_count = 0
      for term, weight in list_of_terms.iteritems():
        if payload.find(term) != -1:
          sum_of_weights += weight
          matched_term_count += 1

      if matched_term_count:
        similarity = float(sum_of_weights) / matched_term_count
        if similarity == max_similarity:
          best_protocols += [protocol]
        elif similarity > max_similarity:
          best_protocols = [protocol]
          max_similarity = similarity

    return best_protocols


def parse_weighted_term_file(
    path, separator='|', top_terms=.1,
    weight_function=weight.CuteWeightFunction):
  """ Parses the files for weighted terms of protocols.

  Args:
    path: The file path.
    separator: The character used to split the columns in the file.
    top_terms: The percentage of top terms for each protocol to return.
    rho: The rho constant of the weight function.
  """
  term_frequency_map = dict() # It is a dictionary of
                              # protocol->frequency->term
  for line in open(path):
    line = line[:-1]
    protocol_end = line.find(separator)
    frequency_end = line.find(separator, protocol_end + 1)
    if frequency_end < -1 or protocol_end < -1:
      continue
    term = line[frequency_end + 1:]
    frequency = line[protocol_end + 1: frequency_end]
    protocol = line[:protocol_end]
    protocol_map = term_frequency_map.get(term, {})
    protocol_map[protocol] = float(frequency)
    term_frequency_map[term] = protocol_map

  return weight_function.weight(term_frequency_map)


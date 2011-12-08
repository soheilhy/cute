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

class WeightFunction(object):
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def weight(self, term_frequency_map):
    return

class CuteWeightFunction(WeightFunction):

  def __init__(self, rho=16, frequency_threshold=0.1):
    self._rho = rho
    self._frequency_threshold = frequency_threshold

  def weight(self, term_frequency_map):
    ''' Extracts the set of weighted terms for each protocol.

    Args:
      term_frequency_map: The term frequency map: term->protocol->frequency.

    Returns:
      Returns a map from protocol->term->weight.
    '''
    protocol_term_count = dict()
    for term, protocol_frequency_map in term_frequency_map.items():
      for protocol, freq in protocol_frequency_map.items():
        p_count = protocol_term_count.get(protocol)
        protocol_term_count[protocol] = p_count + 1 if p_count != None else 1

    protocol_map = {}
    for term, protocol_frequency_map in term_frequency_map.items():
      sum_of_frequencies =\
          sum([freq for protocol, freq in protocol_frequency_map.items()])
      for protocol, freq in protocol_frequency_map.items():
        if freq < self._frequency_threshold:
          continue

        weighted_term_list = protocol_map.get(protocol, dict())
        weighted_term_list[term] = pow(freq / sum_of_frequencies, self._rho)
        protocol_map[protocol] = weighted_term_list
    return protocol_map


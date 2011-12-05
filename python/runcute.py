import getopt
import sys

import cute
import cute.weight

def print_usage():
  print('USAGE: runcute.py -t top_terms -r rho -f frequency_threshold')

if __name__ == '__main__':
  opts, args = getopt.getopt(sys.argv[1:], 't:r:f:')
  if len(args) != 2:
    print_usage()
    sys.exit(-1)


  top_terms = .1
  frequency_threshold = .1
  rho = 16

  for opt, value in opts:
    if opt == '-t':
      top_terms = float(value)
    elif opt == '-f':
      frequency_threshold = float(value)
    elif opt == '-r':
      rho = float(value)

  tf_file = args[0]
  dataset = args[1]

  weighted_terms = cute.parse_weighted_term_file(tf_file, top_terms=top_terms,
      weight_function=cute.weight.CuteWeightFunction(rho, frequency_threshold))
  c = cute.Cute(weighted_terms)
  for data in open(dataset, errors='ignore', encoding='ascii'):
    data = data[:-1]
    protocol_end = data.find('|')
    protocol = data[0:protocol_end]
    payload = data[protocol_end + 1:]

    print('%s|%s|%s' % (protocol, str(c.classify(payload)), payload))

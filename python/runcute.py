import getopt
import sys

import cute
import cute.weight

def print_usage():
  print('USAGE: runcute.py -t top_terms -r rho -f frequency_threshold')

if __name__ == '__main__':
  opts, args = getopt.getopt(sys.argv[1:], 't:r:f:l')
  if len(args) != 1:
    print_usage()
    sys.exit(-1)


  top_terms = .1
  frequency_threshold = .1
  rho = 16
  log_weighted_terms = False

  for opt, value in opts:
    if opt == '-t':
      top_terms = float(value)
    elif opt == '-f':
      frequency_threshold = float(value)
    elif opt == '-r':
      rho = float(value)
    elif opt == '-l':
      log_weighted_terms = True

  tf_file = args[0]

  weighted_terms = cute.parse_weighted_term_file(tf_file, top_terms=top_terms,
      weight_function=cute.weight.CuteWeightFunction(rho, frequency_threshold))

  if log_weighted_terms:
    for protocol, protocol_wterms in weighted_terms.items():
      for term, weight in protocol_wterms.items():
        print('%s|%s|%d' % (protocol, term, weight), file=sys.stderr)
    sys.exit(0)

  dataset = args[1]

  c = cute.Cute(weighted_terms)
  i = 0
  for data in open(dataset, errors='ignore', encoding='ascii'):
    data = data[:-1]
    protocol_end = data.find('|')
    protocol = data[0:protocol_end]
    payload = data[protocol_end + 1:]

    print('%s|%s|%s' % (protocol, str(c.classify(payload)), payload))
    i += 1
    print(i, end='\r', file=sys.stderr)

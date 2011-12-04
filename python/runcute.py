import sys

import cute

if __name__ == '__main__':
  tf_file = sys.argv[1]
  dataset = sys.argv[2]

  weighted_terms = cute.parse_weighted_term_file(tf_file)
  c = cute.Cute(weighted_terms)
  for data in open(dataset, errors='ignore', encoding='ascii'):
    data = data[:-1]
    protocol_end = data.find('|')
    protocol = data[0:protocol_end]
    payload = data[protocol_end + 1:]

    print('%s|%s|%s' % (protocol, str(c.classify(payload)), payload))

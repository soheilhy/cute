import sys

import cute.utils

def parse(line):
  first = line.find('|')
  second = line.find('|', first + 1)
  if first == -1 or second == -1:
    return (None, None, None)

  return (line[0:first], float(line[first+1:second]), line[second+1:])

if __name__ == '__main__':
  min_freq = float(sys.argv[1])
  trie = cute.utils.Trie()
  for line in sys.stdin:
    protocol, frequency, term = parse(line[:-1])
    if not term or frequency < min_freq:
      continue
    def f(t, term):
      existing_freq = t._protocol_count.get(protocol)
      if existing_freq and frequency < existing_freq:
        return
      t._protocol_count[protocol] = frequency
      t._print_protocol[protocol] = len(term) == 1

    trie.add(term, f)

  trie.print_protocol_counts(use_print_flag=True)


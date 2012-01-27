import sys
import cute.utils

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('fastcounter <term_file> <length_threshold>')

  term_file = sys.argv[1]
  length_threshold = int(sys.argv[2])

  trie = cute.utils.Trie()
  for term in open(term_file):
    trie.add(term[:-1])

  for flow in sys.stdin:
    protocol_index = flow.find('|')
    protocol = flow[:protocol_index]
    payload = flow[protocol_index + 1:-1]
    for i in range(0, len(payload) - length_threshold + 1):
      for j in range(i + length_threshold, len(payload) + 1):
        trie.inc_if_contains(payload[i:j], protocol)

  trie.print_protocol_counts()

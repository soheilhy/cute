import sys
import cute.utils

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('fastcounter <term_file> <length_threshold>')

  term_file = sys.argv[1]
  length_threshold = int(sys.argv[2])

  trie = cute.utils.Trie()
  for term in open(term_file):
    trie.add(term[:-1].lower())

  flow_count = 0
  protocol_count = {}
  for flow in sys.stdin:
    flow = flow.lower()
    flow_count = flow_count + 1
    print("flows: %d len: %d\r" % (flow_count, len(flow)), file=sys.stderr)
    protocol_index = flow.find('|')
    protocol = flow[:protocol_index]
    count = protocol_count.get(protocol)
    if not count:
      count = 0
    protocol_count[protocol] = count + 1
    payload = flow[protocol_index + 1:-1]
    for i in range(0, len(payload) - length_threshold + 1):
      #for j in range(i + length_threshold, len(payload) + 1):
      #trie.inc_if_contains(payload, protocol, i, j)
      trie.inc_substrings(payload, protocol, i, len(payload), length_threshold)
  if len(sys.argv) > 3 and sys.argv[3] == 'freq':
    trie.print_protocol_counts(p_count=protocol_count)
  else:
    trie.print_protocol_counts()

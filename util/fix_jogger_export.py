#!/usr/bin/env python3

"""I got a bad export from jogger.pl.

Chrome said:

This page contains the following errors:

  error on line 15428 at column 249: PCDATA invalid Char value 15
  Below is a rendering of the page up to the first error.

The bad value is 15. So let's find all the values 15 and remove them.
"""

import argparse

def main():
  parser = argparse.ArgumentParser("Fix the Jogger XML export")
  parser.add_argument(
      "input_file",
      help="Input XML file. Must be uncompressed.")
  parser.add_argument(
      "output_file",
      help="Output XML file. Will be uncompressed.")
  args = parser.parse_args()
  assert args.input_file != args.output_file
  with open(args.input_file) as in_fd:
    content = in_fd.read()
    new_content = content.replace(chr(15), '')
    if content != new_content:
      print('There was something to fix in the exported XML file.')
    with open(args.output_file, 'w') as out_fd:
      print('Writing the file to disk as %r', args.output_file)
      out_fd.write(new_content)
  print('Done!')

if __name__ == '__main__':
  main()

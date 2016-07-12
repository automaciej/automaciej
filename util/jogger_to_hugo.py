#!/usr/bin/env python3
# vim:set ts=2 sts=2 sw=2:

"""Convert a Jogger.pl XML export to hugo / Markdown.

You need to uncompress the XML file before processing it with this tool.

Installation
------------

E.g. use virtualenv. Then:

pip install python-dateutil
pip install html2text

Then just execute this script.

Missing features:
  - convert body to Markdown from HTML (there seem to libraries out there
    already)
  - export comments too (as an option?)

Use at your own risk!
"""

import xml.etree.ElementTree as ET
import argparse
import dateutil.parser
import html2text
import os.path
import textwrap

def FormatComments(comments):
  result = "# Komentarze\n\n"
  # out_fd.write('# Komentarze\n\n')
  for comment in comments:
    comment_date = dateutil.parser.parse(comment.find('date').text)
    comment_nick = comment.find('nick').text
    comment_body = comment.find('body').text
    item = '%s (%s): %s\n' % (comment_nick, comment_date,
                              comment_body)
    for idx, line in enumerate(textwrap.wrap(item, 78)):
      prefix = '* ' if not idx else '  '
      result += prefix
      result += line
      result += '\n'
  return result


def main():
  parser = argparse.ArgumentParser(__doc__)
  parser.add_argument(
      "input_file",
      help="Input XML file. Must be uncompressed.")
  parser.add_argument(
      "output_directory",
      help="Output directory, where .md files are written.")
  args = parser.parse_args()
  tree = ET.parse(args.input_file)
  root = tree.getroot()
  abs_out_dir = os.path.abspath(args.output_directory)
  for entry in root.findall('entry'):
    date = dateutil.parser.parse(entry.find('date').text)
    permalink = entry.find('permalink').text
    subject = entry.find('subject').text.strip()
    body = entry.find('body').text
    print(date, permalink, "|", subject)
    out_file = os.path.join(abs_out_dir, permalink + '.md')
    with open(out_file, 'w') as out_fd:
      out_fd.write('+++\n')
      out_fd.write('# vim:set nosmartindent nocindent ft=markdown:\n')
      out_fd.write('date = "%s"\n' % date.isoformat())
      out_fd.write('draft = false\n')
      out_fd.write('title = "%s"\n' % subject)
      out_fd.write('+++\n')
      out_fd.write(html2text.html2text(body))
      comments = entry.findall('comment')
      if comments:
        out_fd.write(FormatComments(comments))

if __name__ == '__main__':
  main()

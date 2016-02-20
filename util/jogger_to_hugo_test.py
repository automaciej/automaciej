#!/usr/bin/env python3
# vim:set ts=2 sts=2 sw=2:

"""Unit test for jogger_to_hugo.

Originally written to handle comments better.
"""

import xml.etree.ElementTree as ET
import jogger_to_hugo
import unittest

INPUT_XML_1 = """<?xml version="1.0" encoding="UTF-8"?>
<jogger>
  <user>
    <jid>jid@example.com</jid>
    <domain>automaciej</domain>
    <alias></alias>
  </user>
  <entry>
    <date>2003-12-19 21:17:44</date>
    <jid>jid@example.com</jid>
    <level_id>0</level_id>
    <comment_mode>1</comment_mode>
    <subject>Sprawozdanie z POB</subject>
    <body>&lt;p&gt;Po całym dniu ślęczenia sprawozdanie z POB (Przetwarzanie Obrazów) nareszcie gotowe. Czynności
powtarzalne powinno się wykonywać przy pomocy pętli for, a nie myszką. Jutro i pojutrze po
dwanaście godzin zajęć w szkole. Ale... Don't worry, be happy!&lt;/p&gt;
</body>
    <tags></tags>
    <permalink>sprawozdanie-z-pob</permalink>
    <trackback></trackback>
    <category>szkoła</category>
    <comment>
      <date>2003-12-19 21:45:47</date>
      <nick>kasiaczek</nick>
      <nick_url></nick_url>
      <body>&lt;p&gt;Dobry początek..czekam na ciąg dalszy :-)) DASZ RADĘ, hihi&lt;/p&gt;</body>
      <ip>1.2.3.4</ip>
      <trackback></trackback>
    </comment>
    <comment>
      <date>2009-04-05 18:45:20</date>
      <nick>dasz</nick>
      <nick_url></nick_url>
      <body>&lt;p&gt;hheh jestes boss&lt;/p&gt;</body>
      <ip>5.6.7.8</ip>
      <trackback></trackback>
    </comment>
  </entry>
</jogger>
"""

COMMENTS_RESULT_1 = """# Komentarze

* kasiaczek (2003-12-19 21:45:47): <p>Dobry początek..czekam na ciąg dalszy :-))
  DASZ RADĘ, hihi</p>
* dasz (2009-04-05 18:45:20): <p>hheh jestes boss</p>
"""

class CommentsUnitTest(unittest.TestCase):

  def testOne(self):
    root = ET.fromstring(INPUT_XML_1)
    entry = root.find('entry')
    comments = entry.findall('comment')
    self.assertEqual(COMMENTS_RESULT_1,
                     jogger_to_hugo.FormatComments(comments))


if __name__ == '__main__':
  unittest.main()

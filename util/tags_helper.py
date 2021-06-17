#!/usr/bin/env python3

from typing import Any, Dict, Mapping

import argparse
import logging
import os
import os.path
import re
import toml
import pprint
import yaml

def GetTomlFromFile(content: str) -> Mapping[str, Any]:
    parts = re.split('^\+\+\+\n', content, flags=re.M)
    if len(parts) >= 3:
        return toml.loads(parts[1])
    parts = re.split('^---\n', content, flags=re.M)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1])
    raise ValueError("content doesn't seem supported")

def GetData(directory: str) -> Mapping[str, Any]:
    articles: Dict[str, Any] = {}
    for root, dirs, files in os.walk(directory):
        logging.debug('root: %s', root)
        for f in files:
            if f.startswith('.'):
                continue
            if not f.endswith('.md'):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, 'r') as fd:
                    content = fd.read()
                try:
                    front_matter = GetTomlFromFile(content)
                except ValueError as e:
                    logging.info("%s reading failed: %s", p, e)
                articles[p] = {
                        'front_matter': front_matter,
                        'content': content,
                }
            except UnicodeDecodeError as e:
                logging.error("{} {}".format(p, e))
                raise
    return articles


def Analyze(articles) -> Mapping[str, Any]:
    analysis: Dict[str, Any] = {}
    analysis['Number of articles'] = len(articles)
    without_tags = []
    for p in articles:
        data = articles[p]
        if 'tags' not in data['front_matter']:
            without_tags.append(p)
    analysis['without tags'] = without_tags
    return analysis


def main():
    # print(GetTomlFromFile('content/page/about.md'))
    parser = argparse.ArgumentParser(
       description='Display stats of a hugo content directory')
    parser.add_argument('directory', help='Directory with *.md files')
    args = parser.parse_args()
    articles = GetData(args.directory)
    analysis = Analyze(articles)
    pprint.pprint(analysis)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

#!/usr/bin/env python3

import argparse
import logging
import os
import os.path
import re
import toml
import pprint

def GetTomlFromFile(content):
    parts = re.split('\+\+\+', content, flags=re.M)
    if len(parts) != 3:
        logging.info("%s did not have 3 parts")
        return {}
    return toml.loads(parts[1])

def GetData(directory):
    articles = {}
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
                front_matter = GetTomlFromFile(content)
                articles[p] = {
                        'front_matter': front_matter,
                        'content': content,
                }
            except UnicodeDecodeError as e:
                logging.error("{} {}".format(p, e))
                raise
    return articles


def Analyze(articles):
    analysis = {}
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
    parser = argparse.ArgumentParser(description='Display stats of a hugo '
    'content directory')
    parser.add_argument('directory', help='Directory with *.md files')
    args = parser.parse_args()
    articles = GetData(args.directory)
    analysis = Analyze(articles)
    pprint.pprint(analysis)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

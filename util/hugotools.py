#!/usr/bin/python3

from typing import Any, Dict, Mapping

import collections
import re
import toml
import yaml

class Error(Exception):
    pass


def SplitToml(content):
    return re.split('\+\+\+\n', content, 3, flags=re.M)


def SplitYaml(content):
    return re.split('---\n', content, 3, flags=re.M)


def GetTomlFromContent(content: str) -> Mapping[str, Any]:
    parts = SplitToml(content)
    if len(parts) >= 3:
        return toml.loads(parts[1], _dict=collections.OrderedDict)
    parts = re.split('^---\n', content, flags=re.M)
    if len(parts) >= 3:
        return yaml.safe_load(parts[1])
    raise ValueError("content doesn't seem supported")

def ExtractYaml(content):
    parts = re.split('---\n', content, 3, flags=re.M)
    if len(parts) < 3:
        raise Error('Content did not have 3 parts')
    return yaml.safe_load(parts[1])


def ContentToMetadata(content):
    if content.startswith('---'):
        front_matter = ExtractYaml(content)
    elif content.startswith('+++'):
        front_matter = GetTomlFromContent(content)
    else:
        raise Error("This content doesn't seem to have a separator for front matter.")
    return {
            'front_matter': front_matter,
            'content': content,
    }


def GetPageData(filename):
    try:
        with open(filename, 'r') as fd:
            content = fd.read()
    except UnicodeDecodeError as e:
        logging.error("{} {}".format(p, e))
        raise
    return ContentToMetadata(content)


def ReplaceFrontMatter(content, new_front_matter):
    if content.startswith('---'):
        parts = SplitYaml(content)
        parts[1] = yaml.dump(new_front_matter, allow_unicode=True) + '\n'
        return '---\n'.join(parts)
    elif content.startswith('+++'):
        parts = SplitToml(content)
        parts[1] = toml.dumps(new_front_matter) + '\n'
        return '+++\n'.join(parts)
    else:
        raise Error('Unknown front matter style: ' + content)


def GetBody(content):
    parts = SplitToml(content)
    if len(parts) != 3:
        raise Error("Content %r doesn't have 3 parts." %  content)
    return parts[2]


def ReplaceBody(content, new_body):
    parts = SplitToml(content)
    parts[2] = new_body
    return '+++\n'.join(parts)

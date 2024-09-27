#!/usr/bin/python3

# A script to help move pages from one place to another. The input is from `hugo
# list published` and doesn't need to be edited beyond removing files you don't
# want to touch.

import argparse
import csv
import re
import os.path
import toml

import hugotools

def ProcessPage(page_info, strip_url_part, do_write=False):
    """
    (path, slug, title, date, expiryDate, publishDate, draft, permalink,
    kind, section) = row
    """
    new_path = re.sub('content/post/', 'content/jogger/', page_info['path'])
    new_path = re.sub('content/page/', 'content/jogger/', new_path)
    # print(f'{page_info["path"]!r} -> {new_path!r}')
    if not os.path.isfile(new_path):
        print(f"File {new_path!r} doesn't exist and that's strange.")
        return
    metadata = hugotools.GetPageData(new_path)
    front_matter = metadata['front_matter']
    if 'aliases' not in front_matter:
        front_matter['aliases'] = []
    permalink = page_info['permalink']
    if strip_url_part and not permalink.startswith(strip_url_part):
        raise ValueError(f"Permalink {permalink} not starting with {strip_url_part}?")
    permalink = permalink.lstrip(strip_url_part)
    if not permalink.startswith('/'):
        permalink = '/' + permalink
    while permalink in front_matter['aliases']:
        front_matter['aliases'].remove(permalink)
    front_matter['aliases'].append(permalink)
    print(front_matter)
    new_content = hugotools.ReplaceFrontMatter(metadata['content'], front_matter)
    if do_write:
        with open(new_path, 'w') as fd:
            fd.write(new_content)
    else:
        print(f'Would have written to {new_path}')


def main():
    parser = argparse.ArgumentParser(description='Set aliases to Hugo pages')
    parser.add_argument('input', help='a file with the `hugo list` content')
    parser.add_argument('--write', help='Write results back, in-place',
                        default=False, action='store_true')
    parser.add_argument('--baseurl', help='baseurl to strip',
                        default='https://blizin.ski')
    args = parser.parse_args()

    # File format:
    # path,slug,title,date,expiryDate,publishDate,draft,permalink,kind,section
    with open(args.input, 'r') as fd:
        reader = csv.DictReader(fd, delimiter=',')
        for page_info in reader:
            # This substitution must match the moves you made on the filesystem.
            ProcessPage(page_info, args.baseurl, args.write)

if __name__ == '__main__':
    main()

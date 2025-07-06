# -*- coding: utf-8 -*-
"""
Script for creating rst files for each raw documents.
"""

import re
import glob
import os.path
import lxml.html

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(root_dir, 'raw')
doc_dir = os.path.join(root_dir, 'doc')

def main():
    files = glob.glob("%s/*/*.html" % raw_dir)
    for fpath in files:
        dirs = fpath.split('/')

        # files and dirs
        sub_dir = dirs[-2]
        raw_file = dirs[-1]
        doc_id = raw_file.replace('.html', '')
        rst_file = raw_file.replace('html', 'rst')
        rst_dir = os.path.join(doc_dir, sub_dir)

        # open raw file and get dom
        with open(fpath, encoding='utf-8') as fp:
            html = fp.read()
        doc = lxml.html.fromstring(html)

        # get elements
        title = doc.xpath('//title')[0].text_content()
        body = lxml.html.tostring(doc.xpath('/html/body')[0], encoding='utf-8').decode('utf-8')
        body = re.sub(r'^\W*<body>', '', body)
        body = re.sub(r'</body>\W*$', '', body)

        # rst lines and content
        rst_lines = list()
        rst_lines.append('.. _%s:' % doc_id)
        rst_lines.append('')
        rst_lines.append(':orphan:')
        rst_lines.append('')
        rst_lines.append("=" * (len(title) * 2))
        rst_lines.append(title)
        rst_lines.append("=" * (len(title) * 2))
        rst_lines.append('')
        rst_lines.append('.. raw:: html')
        rst_lines.append(re.sub(r"^", "    ", body, 0, re.MULTILINE))
        rst_lines = [x for x in rst_lines if x != '    ']
        rst_content = "\n".join(rst_lines)
        rst_content += '\n'

        # write to rst file
        if not os.path.exists(rst_dir):
            os.makedirs(rst_dir)

        with open(os.path.join(rst_dir, rst_file), 'w', encoding='utf-8') as rst:
            rst.write(rst_content)
        print("Created %s" % os.path.join(rst_dir, rst_file))

if __name__ == '__main__':
    main()
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
        fp = open(fpath)
        html = fp.read().decode('utf-8')
        fp.close()
        doc = lxml.html.fromstring(html)

        # get elements
        title = doc.xpath('//title')[0].text_content()
        body = lxml.html.tostring(doc.xpath('/html/body')[0], encoding='utf-8').decode('utf-8')
        body = body.replace('<body>', '').replace('</body>', '')

        # rst lines and content
        rst_lines = list()
        rst_lines.append('.. _%s:' % doc_id)
        rst_lines.append('')
        rst_lines.append("=" * (len(title) * 2))
        rst_lines.append(title)
        rst_lines.append("=" * (len(title) * 2))
        rst_lines.append('')
        rst_lines.append('.. raw:: html')
        rst_lines.append(re.sub("^", "    ", body, 0, re.MULTILINE))
        rst_content = "\n".join(rst_lines).encode('utf-8')

        # write to rst file
        if not os.path.exists(rst_dir):
            os.makedirs(rst_dir)

        rst = open(os.path.join(rst_dir, rst_file), 'w')
        rst.write(rst_content)
        rst.close()
        print "Created %s" % os.path.join(rst_dir, rst_file)

if __name__ == '__main__':
    main()

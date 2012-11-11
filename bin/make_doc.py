# -*- coding: utf-8 -*-
"""
Script for creating rst files for each raw documents.
"""

import glob
import os.path

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(root_dir, 'raw')
doc_dir = os.path.join(root_dir, 'doc')

def main():
    files = glob.glob("%s/*/*.html" % raw_dir)
    for f in files:
        dirs = f.split('/')

        # files and dirs
        sub_dir = dirs[-2]
        raw_file = dirs[-1]
        rst_file = raw_file.replace('html', 'rst')
        rst_dir = os.path.join(doc_dir, sub_dir)

        # rst content
        rst_content = ".. raw:: html\n    :file: ../../raw/%s/%s\n" % (sub_dir, raw_file)

        if not os.path.exists(rst_dir):
            os.makedirs(rst_dir)

        rst = open(os.path.join(rst_dir, rst_file), 'w')
        rst.write(rst_content)
        rst.close()
        print "Created %s" % os.path.join(rst_dir, rst_file)

if __name__ == '__main__':
    main()

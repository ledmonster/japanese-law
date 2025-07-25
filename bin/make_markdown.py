# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "html2text",
#     "lxml",
# ]
# ///
# usage: uv run bin/make_markdown.py

# -*- coding: utf-8 -*-
"""
Script for creating markdown files for each raw documents.
"""

import re
import glob
import os.path
import lxml.html
import html2text

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_dir = os.path.join(root_dir, 'raw')
markdown_dir = os.path.join(root_dir, 'markdown')

def convert_html_to_markdown(html_content, title):
    """HTMLをMarkdownに変換"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.body_width = 0  # 改行を制限しない
    h.unicode_snob = True  # Unicode文字を適切に処理
    h.mark_code = True  # コードブロックをマークダウン形式に
    
    # bodyタグ内のコンテンツのみを変換
    body_markdown = h.handle(html_content)
    
    # タイトル付きMarkdown作成
    markdown_content = f"# {title}\n\n"
    markdown_content += body_markdown
    
    return markdown_content

def main():
    files = glob.glob("%s/*/*.html" % raw_dir)
    for fpath in files:
        dirs = fpath.split('/')

        # files and dirs
        sub_dir = dirs[-2]
        raw_file = dirs[-1]
        doc_id = raw_file.replace('.html', '')
        md_file = raw_file.replace('.html', '.md')
        md_dir = os.path.join(markdown_dir, sub_dir)

        # open raw file and get dom
        with open(fpath, encoding='utf-8') as fp:
            html = fp.read()
        doc = lxml.html.fromstring(html)

        # get elements
        title = doc.xpath('//title')[0].text_content()
        body = lxml.html.tostring(doc.xpath('/html/body')[0], encoding='utf-8').decode('utf-8')
        
        # bodyタグを除去してコンテンツのみ抽出
        body = re.sub(r'^\W*<body[^>]*>', '', body)
        body = re.sub(r'</body>\W*$', '', body)

        # HTMLをMarkdownに変換
        markdown_content = convert_html_to_markdown(body, title)

        # write to markdown file
        if not os.path.exists(md_dir):
            os.makedirs(md_dir)

        with open(os.path.join(md_dir, md_file), 'w', encoding='utf-8') as md:
            md.write(markdown_content)
        print("Created %s" % os.path.join(md_dir, md_file))

if __name__ == '__main__':
    main()

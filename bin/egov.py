# -*- coding: utf-8 -*-
import re
import cmd
import os
import os.path
import lxml.html
import json
import urllib.request

class Egov(cmd.Cmd):
    """ Interactive command line interface for e-gov. """
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    categories = [
        (1, "憲法"), (2, "刑事"), (3, "財務通則"), (4, "水産業"), (5, "観光"),
        (6, "国会"), (7, "警察"), (8, "国有財産"), (9, "鉱業"), (10, "郵務"),
        (11, "行政組織"), (12, "消防"), (13, "国税"), (14, "工業"), (15, "電気通信"),
        (16, "国家公務員"), (17, "国土開発"), (18, "事業"), (19, "商業"), (20, "労働"),
        (21, "行政手続"), (22, "土地"), (23, "国債"), (24, "金融・保険"), (25, "環境保全"),
        (26, "統計"), (27, "都市計画"), (28, "教育"), (29, "外国為替・貿易"), (30, "厚生"),
        (31, "地方自治"), (32, "道路"), (33, "文化"), (34, "陸運"), (35, "社会福祉"),
        (36, "地方財政"), (37, "河川"), (38, "産業通則"), (39, "海運"), (40, "社会保険"),
        (41, "司法"), (42, "災害対策"), (43, "農業"), (44, "航空"), (45, "防衛"),
        (46, "民事"), (47, "建築・住宅"), (48, "林業"), (49, "貨物運送"), (50, "外事"),
        ]

    intro = '''\nThis is an interactive commandline interface for e-gov.\nhttp://law.e-gov.go.jp/cgi-bin/idxsearch.cgi '''
    prompt = 'egov> '

    def emptyline(self):
        self.do_help(None)

    def do_list(self, line):
        """
        get a list of documents for category.
        usage: list <category_key>
        """
        try:
            key = int(line.strip())
            if key not in dict(self.categories):
                print("usage: list <category_key>\n")
                self._show_categories()
        except ValueError:
            print("usage: list <category_key>\n")
            self._show_categories()
            return False

        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}&limit=1000"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            for law in data.get('laws', []):
                revision_info = law.get('revision_info', {})
                law_revision_id = revision_info.get('law_revision_id')
                law_title = revision_info.get('law_title')
                if law_revision_id and law_title:
                    print(f"{law_revision_id}: {law_title}")

    def do_mklist(self, line):
        """
        make category index rst from e-gov
        usage: mklist <category_key>
        """
        try:
            key = int(line.strip())
            if key not in dict(self.categories):
                print("usage: mklist <category_key>\n")
                self._show_categories()
        except ValueError:
            print("usage: mklist <category_key>\n")
            self._show_categories()
            return False

        # lines for category rst
        lines = list()

        # title
        title = dict(self.categories)[key]
        lines.append("=" * (len(title) * 2))
        lines.append(title)
        lines.append("=" * (len(title) * 2))
        lines.append("")

        # documents
        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}&limit=1000"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            for law in data.get('laws', []):
                revision_info = law.get('revision_info', {})
                doc_id = revision_info.get('law_revision_id')
                doc_title = revision_info.get('law_title')
                if doc_id and doc_title:
                    lines.append("* :doc:`%s <../doc/%s/%s>`" % (doc_title, doc_id[:3], doc_id))

        # last line
        lines.append("")

        # write to file
        cat_dir = os.path.join(self.root_dir, "cat")
        with open(os.path.join(cat_dir, "%d.rst" % key), 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))

    def do_get(self, line):
        """
        get a document by document id
        usage: get <document_id>
        """
        if not line.strip():
            print("usage: get <document_id>\n")

        key = line.strip()
        url = f"https://laws.e-gov.go.jp/api/2/law_file/html/{key}"
        with urllib.request.urlopen(url) as response:
            doc = lxml.html.parse(response).getroot()
            print("get: %s" % url)
            print(lxml.html.tostring(doc.body, encoding='utf-8').decode('utf-8'))

    def do_fetch(self, line):
        """
        fetch documents from e-gov by category key and save it to raw directory.
        usage:  fetch <category_key>
        """
        try:
            key = int(line.strip())
            if key not in dict(self.categories):
                print("usage: fetch <category_key>")
                return False
        except ValueError:
            print("usage: fetch <category_key>")
            return False

        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}&limit=1000"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            for law in data.get('laws', []):
                revision_info = law.get('revision_info', {})
                document_id = revision_info.get('law_revision_id')
                if document_id:
                    self.do_fetchdoc(document_id)

    def do_fetchdoc(self, line):
        """
        fetch documents from e-gov by document id and save it to raw directory.
        usage:  fetchdoc <document_id>
        """
        if not line.strip():
            print("usage: fetchdoc <document_id>\n")

        key = line.strip()
        url = "https://laws.e-gov.go.jp/api/2/law_file/html/%s" % key

        print("fetchdoc: %s" % url)
        with urllib.request.urlopen(url) as response:
            doc = lxml.html.parse(response).getroot()
        content = lxml.html.tostring(doc, encoding='utf-8')

        filedir = os.path.join(self.root_dir, "raw", key[:3])
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        filepath = os.path.join(filedir, "%s.html" % key)

        with open(filepath, 'wb') as f_out:
            f_out.write(content)

    def do_EOF(self, line):
        """ exit shell """
        return True

    def do_bye(self, line):
        """ exit shell """
        return True

    def _show_categories(self):
        """ show a list of categories and their keys """
        for i, (key, val) in enumerate(self.categories, 1):
            separator = '\n' if i % 5 == 0 else ' ' * (15 - len(val) * 2)
            print('%02s: %s%s' % (key, val, separator), end='')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # print(' '.join(sys.argv[1:]))
        Egov().onecmd(' '.join(sys.argv[1:]))
    else:
        Egov().cmdloop()

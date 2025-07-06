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
        (1, "憲　法"), (2, "国　会"), (3, "行政組織"), (4, "国家公務員"), (5, "行政手続"),
        (6, "統　計"), (7, "地方自治"), (8, "地方財政"), (9, "司　法"), (10, "民　事"),
        (11, "刑　事"), (12, "警　察"), (13, "消　防"), (14, "国土開発"), (15, "土　地"),
        (16, "都市計画"), (17, "道　路"), (18, "河　川"), (19, "災害対策"), (20, "建築・住宅"),
        (21, "財務通則"), (22, "国有財産"), (23, "国　税"), (24, "事　業"), (25, "国　債"),
        (26, "教　育"), (27, "文　化"), (28, "産業通則"), (29, "農　業"), (30, "林　業"),
        (31, "水産業"), (32, "鉱　業"), (33, "工　業"), (34, "商　業"), (35, "金融・保険"),
        (36, "外国為替・貿易"), (37, "陸　運"), (38, "海　運"), (39, "航　空"), (40, "貨物運送"),
        (41, "観　光"), (42, "郵　務"), (43, "電気通信"), (44, "労　働"), (45, "環境保全"),
        (46, "厚　生"), (47, "社会福祉"), (48, "社会保険"), (49, "防　衛"), (50, "外　事"),
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

        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}"
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
        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}"
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

        url = f"https://laws.e-gov.go.jp/api/2/laws?category_cd={key:03}"
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

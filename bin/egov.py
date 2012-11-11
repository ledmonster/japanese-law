# -*- coding: utf-8 -*-
import re
import cmd
import lxml.html

class Egov(cmd.Cmd):
    """ Interactive command line interface for e-gov. """
    base_list_url = "http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi?H_CTG_%d=foo&H_CTG_GUN=2&H_NO_GENGO=H&H_NO_TYPE=2&H_RYAKU=1&H_YOMI_GUN=1"
    base_doc_url = "http://law.e-gov.go.jp/htmldata/%s/%s.html"
    categories = [
        (1, u"憲　法"), (2, u"国　会"), (3, u"行政組織"), (4, u"国家公務員"), (5, u"行政手続"),
        (6, u"統　計"), (7, u"地方自治"), (8, u"地方財政"), (9, u"司　法"), (10, u"民　事"),
        (11, u"刑　事"), (12, u"警　察"), (13, u"消　防"), (14, u"国土開発"), (15, u"土　地"),
        (16, u"都市計画"), (17, u"道　路"), (18, u"河　川"), (19, u"災害対策"), (20, u"建築・住宅"),
        (21, u"財務通則"), (22, u"国有財産"), (23, u"国　税"), (24, u"事　業"), (25, u"国　債"),
        (26, u"教　育"), (27, u"文　化"), (28, u"産業通則"), (29, u"農　業"), (30, u"林　業"),
        (31, u"水産業"), (32, u"鉱　業"), (33, u"工　業"), (34, u"商　業"), (35, u"金融・保険"),
        (36, u"外国為替・貿易"), (37, u"陸　運"), (38, u"海　運"), (39, u"航　空"), (40, u"貨物運送"),
        (41, u"観　光"), (42, u"郵　務"), (43, u"電気通信"), (44, u"労　働"), (45, u"環境保全"),
        (46, u"厚　生"), (47, u"社会福祉"), (48, u"社会保険"), (49, u"防　衛"), (50, u"外　事"),
        ]

    intro = '''\
This is an interactive commandline interface for e-gov.
http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi '''
    prompt = 'egov> '

    def do_list(self, line):
        """ get a list of documents for category. """
        try:
            key = int(line.strip())
            if key not in dict(self.categories).keys():
                self._show_categories()
        except ValueError:
            self._show_categories()
            return False

        url = self.base_list_url % key
        doc = lxml.html.parse(url).getroot()
        for link in doc.xpath('//ol/li/p/a'):
            content = link.text_content()
            href = link.get('href')
            matched = re.search(r"H_FILE_NAME=(\w+)&", href)
            filename = matched and matched.group(1) or "UNKNOWN"
            print "%s: %s" % (filename, content)

    def do_get(self, line):
        """ get a document by document id """
        if not line.strip():
            print "usage: get <document_id>\n"

        key = line.strip()
        url = self.base_doc_url % (key[:3], key)
        doc = lxml.html.parse(url).getroot()

        print "get: %s" % url
        print lxml.html.tostring(doc.body, encoding='utf-8')


    def do_EOF(self, line):
        """ exit shell """
        return True

    def do_bye(self, line):
        """ exit shell """
        return True

    def _show_categories(self):
        """ show a list of categories and their keys """
        print "usage: list <category_key>\n"
        for (key, val) in self.categories:
            separator = key % 5 == 0 and "\n" or ' ' * (15 - len(val) * 2)
            print '%02s: %s%s' % (key, val, separator),


if __name__ == '__main__':
    Egov().cmdloop()

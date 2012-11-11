==========
日本の法令
==========

日本の法令を github で管理するプロジェクトです。
総務省の公開している `e-Gov <http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi>`_ から法令情報を fetch して Sphinx 文書へ整形し、readthedocs で公開することを中間目標としています。

----------------
ディレクトリ構成
----------------

Sphinx の基本構成に加え、以下のディレクトリを配置しています。

* /bin: 各種ユーティリティ
* /raw: e-Gov から取得した法令HTML

-------
Utility
-------

egov.py
=======

e-Gov から法令情報を取得することを目的としたインタラクティブツールです。

Requirements
------------

* lxml

Commands
--------

list <category_key>
  category_key に属する文書の一覧を表示します。category_key が指定されなかった場合、category_key の一覧を表示します。

get <document_id>
  指定した document_id の法令文書を表示します。

fetch <category_key>
  指定した category_key に属する文書を e-Gov から取得して、raw ディレクトリに格納します。

fetchdoc <document_id>
  指定した doc_id の文書を e-Gov から取得して、raw ディレクトリに格納します。

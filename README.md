# 日本の法令

日本の法令を github で管理するプロジェクトです。
総務省の公開している [e-Gov](http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi) から法令情報を fetch して Sphinx 文書へ整形し、readthedocs で公開することを中間目標としています。

## コンパイル済み文書

GitHub Pages で公開しています。

* http://ledmonster.github.io/japanese-law/

## ディレクトリ構成

Sphinx の基本構成に加え、以下のディレクトリを配置しています。

* /bin: 各種ユーティリティ
* /raw: e-Gov から取得した法令HTML

## Utility

### egov.py

e-Gov から法令情報を取得することを目的としたインタラクティブツールです。

#### Requirements

* lxml

#### Commands

**list <category_key>**
  category_key に属する文書の一覧を表示します。category_key が指定されなかった場合、category_key の一覧を表示します。

**get <document_id>**
  指定した document_id の法令文書を表示します。

**fetch <category_key>**
  指定した category_key に属する文書を e-Gov から取得して、raw ディレクトリに格納します。

**fetchdoc <document_id>**
  指定した doc_id の文書を e-Gov から取得して、raw ディレクトリに格納します。

**mklist <category_key>**
  e-Gov を元にカテゴリ文書一覧用 rst ファイルを生成します。

## データ更新方法

各カテゴリの文書ファイルを取得

```
for i in $(seq 1 50); do uv run bin/egov.py fetch $i; done
```

各カテゴリの文書一覧を生成

```
for i in $(seq 1 50); do uv run bin/egov.py mklist $i; done
```

raw ファイルをもとに doc ディレクトリに rst ファイルを生成

```
uv run ./bin/make_doc.py
```

sphinx 文書ファイルを生成

```
uv run sphinx-build -E -b html -d _build/doctrees   . _build/html
```

gh-pages を更新
```
git checkout gh-pages
cp -r _build/html/* .
git add doc cat _static _sources
```

# Notion Util

このプロジェクトは、Notion.soの非公式Python APIクライアントです。
NotionページのMarkdown変換やNotion Databaseのcsv変換が可能です。

## インストール

このパッケージをインストールするには、以下のコマンドを実行してください。
```bash
pip install notion-util
```

## 使い方

```bash
export NOTION_SECRET=secret_xxxxxxxxxxxx
```

```python
from notion_util import NotionUtil

# notion page url
url = "https://www.notion.so/xxxx"

notion = NotionUtil()
markdown_content = notion.get_page_markdown(url, recursive=False)
print(markdown_content)
```


```python
from notion_util import Notion, markdown_to_notion_blocks

notion = Notion()
# ここで、NotionのデータベースIDと新しいページのタイトルを指定する
database_id = os.getenv("DATABASE_ID")
page_title = "New Page From Markdown"
# Notionのプロパティを設定
properties = {"URL": {"url": "http://example.com"}}
# 新しいページを作成
res = notion.create_notion_page(database_id, page_title, properties)
# Markdownファイルを読み込む
with open("README.md", "r") as md_file:
    # MarkdownをNotionブロックに変換
    blocks = markdown_to_notion_blocks(md_file.read())
    # Notionページにブロックを追加
    notion.append_blocks_to_page(res["id"], blocks)
```

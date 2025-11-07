# Docling OCR

IBM Researchが提供する`docling`ライブラリを使用したPDF OCR処理。

## 特徴

- **提供元**: IBM Research
- **ライセンス**: MIT
- **特徴**: 高度なドキュメント構造解析、Markdown出力対応
- **利点**: ローカル実行可能、構造化された出力、テーブル認識
- **用途**: レイアウトを保持したテキスト抽出

## セットアップ

```bash
cd docling
pip install -r requirements.txt
```

## 使い方

### 基本的な使用方法

```bash
# PDFからテキストとMarkdownを抽出
python ocr_processor.py ../sample_pdfs/your.pdf output.txt
# → output.txt と output.md が生成されます
```

### Pythonコードから使用

```python
from ocr_processor import DoclingOCR

ocr = DoclingOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

print(f"Extracted {result['char_count']} characters")
print("Text:", result['text'])
print("Markdown:", result['markdown'])
```

## 出力形式

- **テキスト**: プレーンテキストファイル
- **Markdown**: Markdown形式（見出し、リスト、テーブルなど構造を保持）

## 主な機能

- 高精度なテキスト抽出
- ドキュメント構造の保持
- テーブルの認識と抽出
- 画像とテキストの位置関係を保持
- Markdown形式での出力

## 対応フォーマット

- PDF
- Word (docx)
- PowerPoint (pptx)
- HTML
- 画像ファイル

## 参考リンク

- [Docling Documentation](https://ds4sd.github.io/docling/)
- [Docling GitHub](https://github.com/DS4SD/docling)

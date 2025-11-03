# MarkItDown OCR

Microsoftが提供する`markitdown`ライブラリを使用したPDF OCR処理。

## 特徴

- **提供元**: Microsoft
- **ライセンス**: MIT
- **特徴**: シンプルで使いやすい、多様なドキュメント形式に対応
- **利点**: ローカル実行可能、クラウドAPIキー不要
- **用途**: 基本的なテキスト抽出

## セットアップ

```bash
cd markitdown
pip install -r requirements.txt
```

## 使い方

### 基本的な使用方法

```bash
# PDFからテキストを抽出
python ocr_processor.py ../sample_pdfs/your.pdf output.txt
```

### Pythonコードから使用

```python
from ocr_processor import MarkItDownOCR

ocr = MarkItDownOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

print(f"Extracted {result['char_count']} characters")
print(result['text'])
```

## 出力形式

- プレーンテキストファイル
- 元のドキュメントの構造を可能な限り保持

## 対応フォーマット

- PDF
- Word (docx)
- PowerPoint (pptx)
- Excel (xlsx)
- 画像 (png, jpg, jpeg)
- HTML
- その他多数

## 参考リンク

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)

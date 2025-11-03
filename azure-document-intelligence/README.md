# Azure Document Intelligence OCR

Microsoftの`Azure Document Intelligence`（旧Form Recognizer）を使用したPDF OCR処理。

## 特徴

- **提供元**: Microsoft Azure
- **特徴**: 高精度OCR、表やフォームの認識、レイアウト解析
- **利点**: 非常に高い認識精度、多言語対応、クラウドの強力な処理能力
- **用途**: プロダクション環境での高精度OCR

## セットアップ

### 1. Azureリソースの作成

Azure Portal で Document Intelligence リソースを作成し、エンドポイントとAPIキーを取得します。

### 2. 環境変数の設定

```bash
cd azure-document-intelligence

# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAzure認証情報を設定
# AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
# AZURE_DOCUMENT_INTELLIGENCE_KEY=your-key-here
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方

### 基本的な使用方法

```bash
# 基本的なテキスト抽出（prebuilt-read モデル）
python ocr_processor.py ../sample_pdfs/your.pdf output.txt

# レイアウト情報を含む抽出（prebuilt-layout モデル）
python ocr_processor.py ../sample_pdfs/your.pdf output.txt prebuilt-layout

# ドキュメント全体の構造解析（prebuilt-document モデル）
python ocr_processor.py ../sample_pdfs/your.pdf output.txt prebuilt-document
```

### Pythonコードから使用

```python
from ocr_processor import AzureDocumentIntelligenceOCR

ocr = AzureDocumentIntelligenceOCR()
result = ocr.process_pdf("input.pdf", "output.txt", model="prebuilt-read")

print(f"Extracted {result['char_count']} characters from {len(result['pages'])} pages")
print(result['text'])
```

## 利用可能なモデル

| モデル | 説明 | 用途 |
|--------|------|------|
| `prebuilt-read` | 基本的なテキスト抽出 | シンプルなOCR処理 |
| `prebuilt-layout` | レイアウト情報を含む抽出 | テーブルや構造を保持 |
| `prebuilt-document` | ドキュメント全体の構造解析 | 複雑なドキュメント処理 |
| `prebuilt-invoice` | 請求書の解析 | 請求書データ抽出 |
| `prebuilt-receipt` | レシートの解析 | レシートデータ抽出 |

## 出力形式

- ページごとに区切られたテキスト
- 高精度な文字認識
- 多言語サポート（日本語含む）

## 主な機能

- 高精度な文字認識
- テーブルの検出と抽出
- フォームフィールドの認識
- 手書き文字の認識
- 多言語対応（100以上の言語）
- レイアウト情報の保持

## 料金

従量課金制です。詳細は[Azure pricing](https://azure.microsoft.com/ja-jp/pricing/details/form-recognizer/)をご確認ください。

## 参考リンク

- [Azure Document Intelligence](https://azure.microsoft.com/ja-jp/products/ai-services/ai-document-intelligence)
- [Document Intelligence Documentation](https://learn.microsoft.com/ja-jp/azure/ai-services/document-intelligence/)
- [Python SDK Documentation](https://learn.microsoft.com/ja-jp/python/api/overview/azure/ai-documentintelligence-readme)

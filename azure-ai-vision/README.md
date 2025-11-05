# Azure AI Vision OCR

MicrosoftのAzure AI Vision（旧Computer Vision）のRead APIを使用したPDF OCR処理。

## 特徴

- **提供元**: Microsoft Azure
- **API**: Read API (OCR特化)
- **特徴**: 高精度なテキスト認識、印刷/手書き文字の両対応
- **利点**: 高速処理、高精度、多言語対応（164言語）
- **用途**: 高精度OCR、大量ドキュメント処理

## Azure AI Vision vs Document Intelligence

| 機能 | Azure AI Vision | Document Intelligence |
|------|----------------|----------------------|
| **用途** | 画像からのOCR | ドキュメント全体の分析 |
| **テキスト抽出** | ○ | ○ |
| **レイアウト分析** | △ | ◎ |
| **表の認識** | × | ◎ |
| **フォーム認識** | × | ◎ |
| **処理速度** | 速い | 中 |
| **価格** | 低価格 | 高価格 |

**Azure AI Visionを選ぶべき場合:**
- シンプルなテキスト抽出のみが必要
- コストを抑えたい
- 高速処理が必要

**Document Intelligenceを選ぶべき場合:**
- 表やフォームの構造を保持したい
- レイアウト情報が重要
- ドキュメント全体の構造解析が必要

## セットアップ

### 1. Azureリソースの作成

Azure Portal で Computer Vision リソースを作成し、エンドポイントとAPIキーを取得します。

### 2. 追加の依存関係

PDFを画像に変換するために`poppler`が必要です：

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
https://github.com/oschwartz10612/poppler-windows/releases/ からダウンロードしてPATHに追加

### 3. 環境変数の設定

```bash
cd azure-ai-vision

# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAzure認証情報を設定
# AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
# AZURE_VISION_KEY=your-key-here
```

### 4. 依存パッケージのインストール

```bash
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
from ocr_processor import AzureAIVisionOCR

ocr = AzureAIVisionOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

print(f"Extracted {result['char_count']} characters from {len(result['pages'])} pages")
print(result['text'])
```

## 処理の流れ

1. PDFを各ページごとの画像に変換
2. 各画像をAzure AI Vision Read APIで処理
3. 抽出されたテキストを結合
4. ファイルに保存

## 出力形式

- ページごとに区切られたテキスト
- 高精度な文字認識結果
- 行単位でのテキスト抽出

## 主な機能

- 印刷文字の認識（164言語対応）
- 手書き文字の認識（英語）
- 複雑なレイアウトの処理
- 画像内のテキストの位置情報
- 高速処理

## 対応言語

164言語に対応（日本語、英語、中国語、韓国語など）

完全なリストは[公式ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-services/computer-vision/language-support)を参照。

## 料金

従量課金制です。

- **Read API**: 1,000トランザクションあたり $1.00（標準）
- 無料枠: 月5,000トランザクションまで

詳細は[Azure pricing](https://azure.microsoft.com/ja-jp/pricing/details/cognitive-services/computer-vision/)をご確認ください。

## 長所と短所

### 長所
- 高精度なOCR
- 高速処理
- コストパフォーマンスが良い
- 多言語対応
- 手書き文字認識

### 短所
- 表の構造認識は限定的
- フォーム認識には非対応
- レイアウト情報は簡易的

## パフォーマンス

- 処理速度: 1ページあたり約1〜2秒
- 精度: 非常に高い（印刷文字）
- 並列処理: 可能（複数画像を同時処理）

## 参考リンク

- [Azure AI Vision](https://azure.microsoft.com/ja-jp/products/ai-services/ai-vision)
- [Read API Documentation](https://learn.microsoft.com/ja-jp/azure/ai-services/computer-vision/concept-ocr)
- [Python SDK Documentation](https://learn.microsoft.com/ja-jp/python/api/overview/azure/ai-vision-imageanalysis-readme)
- [Language Support](https://learn.microsoft.com/ja-jp/azure/ai-services/computer-vision/language-support)

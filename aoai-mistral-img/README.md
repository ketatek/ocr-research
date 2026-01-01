# Azure OpenAI (Mistral) OCR

Azure OpenAI ServiceのMistralモデルのVision機能を使用したPDF OCR処理。

## 特徴

- **提供元**: Azure OpenAI Service
- **モデル**: Mistral Large (Vision対応)
- **特徴**: LLMのVision機能を使用、文脈理解が可能
- **利点**: 複雑なレイアウトの理解、質問応答可能、文脈を考慮した抽出
- **用途**: 高度な文書理解が必要な場合、複雑なレイアウトのドキュメント

## セットアップ

### 1. Azureリソースの作成

1. Azure Portal で Azure OpenAI Service リソースを作成
2. Mistral Large モデルをデプロイ（Vision対応版）
3. エンドポイントとAPIキーを取得

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
cd azure-openai-mistral

# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAzure認証情報を設定
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-key-here
# AZURE_OPENAI_DEPLOYMENT_NAME=mistral
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
from ocr_processor import AzureOpenAIOCR

ocr = AzureOpenAIOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

print(f"Extracted {result['char_count']} characters from {len(result['pages'])} pages")
print(result['text'])
```

## 処理の流れ

1. PDFを各ページごとの画像に変換
2. 各画像をBase64エンコード
3. Azure OpenAI Vision APIに送信
4. LLMがテキストを抽出して返却
5. 全ページのテキストを結合

## 出力形式

- ページごとに区切られたテキスト
- LLMによる文脈を考慮したテキスト抽出
- 複雑なレイアウトにも対応

## 主な機能

- 高度な文脈理解
- 複雑なレイアウトの処理
- 手書き文字の認識
- 多言語対応
- 画像内の要素の説明も可能

## 料金

従量課金制です。Vision APIの利用は通常のテキスト生成より高額になる場合があります。
詳細は[Azure OpenAI pricing](https://azure.microsoft.com/ja-jp/pricing/details/cognitive-services/openai-service/)をご確認ください。

## 長所と短所

### 長所
- 文脈を理解した高度なテキスト抽出
- 複雑なレイアウトに強い
- プロンプトでカスタマイズ可能
- 質問応答などの応用が可能

### 短所
- 処理速度が遅い（LLM呼び出しのため）
- コストが高い
- ページ数が多い文書では時間がかかる

## カスタマイズ

`ocr_processor.py`の`_extract_text_from_image`メソッド内のシステムプロンプトを変更することで、抽出の挙動をカスタマイズできます：

```python
# 例: 特定の情報のみを抽出
"content": "Extract only the names, dates, and amounts from this invoice image."
```

## 参考リンク

- [Azure OpenAI Service](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)
- [Mistral AI](https://mistral.ai/)
- [Azure OpenAI Vision Documentation](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/gpt-with-vision)

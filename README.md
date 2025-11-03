# OCR Research

OCR（光学文字認識）技術の各種ライブラリとサービスを比較検証するためのリポジトリです。

## 概要

このプロジェクトでは、以下の4つのOCRソリューションを使用してPDFファイルからテキストを抽出し、その精度とパフォーマンスを比較します：

1. **MarkItDown** - Microsoftが提供するドキュメント変換ライブラリ
2. **Docling** - IBM Researchが提供する高度なドキュメント処理ライブラリ
3. **Azure Document Intelligence** - Azureの高精度ドキュメント分析サービス
4. **Azure OpenAI (Mistral)** - Vision機能を使ったLLMベースのOCR

## プロジェクト構造

```
ocr-research/
├── src/                           # ソースコード
│   ├── markitdown_ocr.py         # MarkItDown実装
│   ├── docling_ocr.py            # Docling実装
│   ├── azure_document_intelligence.py  # Azure DI実装
│   └── azure_openai_ocr.py       # Azure OpenAI実装
├── config/                        # 設定ファイル
│   ├── config.yaml               # アプリケーション設定
│   └── .env.example              # 環境変数サンプル
├── tests/                         # テストファイル
│   └── sample_pdfs/              # サンプルPDF格納用
├── output/                        # OCR結果出力先
├── logs/                          # ログファイル
├── requirements.txt               # Python依存パッケージ
├── main.py                        # メインスクリプト
└── README.md                      # このファイル
```

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd ocr-research
```

### 2. Python環境のセットアップ

Python 3.8以上が必要です。

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定

Azure サービスを使用する場合は、環境変数を設定する必要があります。

```bash
# .envファイルを作成
cp config/.env.example .env

# .envファイルを編集して、以下の情報を設定
# - Azure Document Intelligence のエンドポイントとAPIキー
# - Azure OpenAI のエンドポイント、APIキー、デプロイメント名
```

必要な環境変数：

```bash
# Azure Document Intelligence
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-key-here

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=mistral
```

## 使い方

### 基本的な使用方法

```bash
# すべての方法でPDFを処理
python main.py path/to/your.pdf

# 特定の方法のみを使用
python main.py path/to/your.pdf -m markitdown docling

# 出力ディレクトリを指定
python main.py path/to/your.pdf -o custom_output

# 比較レポートを生成
python main.py path/to/your.pdf --compare

# 詳細ログを表示
python main.py path/to/your.pdf -v
```

### コマンドライン引数

- `pdf_path`: 処理するPDFファイルのパス（必須）
- `-o, --output`: 出力ディレクトリ（デフォルト: `output`）
- `-m, --methods`: 使用するOCR方法（`markitdown`, `docling`, `azure_di`, `azure_openai`, `all`）
- `--compare`: すべての方法で処理して結果を比較
- `-v, --verbose`: 詳細ログを表示

### 個別のモジュールを使用

各OCRモジュールは個別に実行することもできます：

```bash
# MarkItDown
python src/markitdown_ocr.py input.pdf output.txt

# Docling
python src/docling_ocr.py input.pdf output.txt

# Azure Document Intelligence
python src/azure_document_intelligence.py input.pdf output.txt

# Azure OpenAI
python src/azure_openai_ocr.py input.pdf output.txt
```

## 各ライブラリの特徴

### MarkItDown
- **提供元**: Microsoft
- **特徴**: シンプルで使いやすい、多様なドキュメント形式に対応
- **利点**: ローカル実行可能、クラウドAPIキー不要
- **用途**: 基本的なテキスト抽出

### Docling
- **提供元**: IBM Research
- **特徴**: 高度なドキュメント構造解析、Markdown出力対応
- **利点**: ローカル実行可能、構造化された出力
- **用途**: レイアウトを保持したテキスト抽出

### Azure Document Intelligence
- **提供元**: Microsoft Azure
- **特徴**: 高精度OCR、表やフォームの認識
- **利点**: 非常に高い認識精度、多言語対応
- **用途**: プロダクション環境での高精度OCR

### Azure OpenAI (Mistral)
- **提供元**: Azure OpenAI Service
- **特徴**: LLMのVision機能を使用、文脈理解が可能
- **利点**: 複雑なレイアウトの理解、質問応答可能
- **用途**: 高度な文書理解が必要な場合

## 出力

各OCR方法の処理結果は、指定した出力ディレクトリに保存されます：

```
output/
├── document_markitdown.txt        # MarkItDownの結果
├── document_docling.txt           # Doclingの結果（テキスト）
├── document_docling.md            # Doclingの結果（Markdown）
├── document_azure_di.txt          # Azure DIの結果
├── document_azure_openai.txt      # Azure OpenAIの結果
└── comparison_report.txt          # 比較レポート（--compareオプション使用時）
```

## トラブルシューティング

### ライブラリのインストールエラー

一部のライブラリは追加の依存関係が必要な場合があります：

```bash
# pdf2image用（PDFを画像に変換）
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows
# https://github.com/oschwartz10612/poppler-windows/releases/ からダウンロード
```

### Azure APIエラー

- エンドポイントURLとAPIキーが正しいか確認してください
- Azure リソースが正しくデプロイされているか確認してください
- ネットワーク接続を確認してください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

Issue や Pull Request を歓迎します。

## 参考リンク

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [Docling Documentation](https://ds4sd.github.io/docling/)
- [Azure Document Intelligence](https://azure.microsoft.com/ja-jp/products/ai-services/ai-document-intelligence)
- [Azure OpenAI Service](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)

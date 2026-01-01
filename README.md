# OCR Research

OCR（光学文字認識）技術の各種ライブラリとサービスを比較検証するためのリポジトリです。

## 概要

このプロジェクトでは、以下の7つのOCRソリューションを個別に検証できます：

1. **[MarkItDown](./markitdown/)** - Microsoftが提供するドキュメント変換ライブラリ
2. **[Docling](./docling/)** - IBM Researchが提供する高度なドキュメント処理ライブラリ
3. **[Azure AI Vision](./azure-ai-vision/)** - Azure Computer VisionのRead API（OCR特化）
4. **[Azure Document Intelligence](./azure-document-intelligence/)** - Azureの高精度ドキュメント分析サービス
5. **[Azure OpenAI Mistral (PDF)](./aoai-mistral-pdf/)** - Mistral OCRモデル（PDF直接処理）
6. **[Azure OpenAI Mistral (Image)](./aoai-mistral-img/)** - Mistral Visionモデル（画像ベース処理）
7. **[MS Foundry Multimodal](./ms-foundry-multimodal/)** - AI Foundryのマルチモーダルモデル（GPT-4V, Phi-3-visionなど）

## プロジェクト構造

```
ocr-research/
├── markitdown/                    # MarkItDown実装
│   ├── README.md                  # 詳細ドキュメント
│   ├── requirements.txt           # 依存パッケージ
│   └── ocr_processor.py           # 実装コード
│
├── docling/                       # Docling実装
│   ├── README.md
│   ├── requirements.txt
│   └── ocr_processor.py
│
├── azure-ai-vision/               # Azure AI Vision実装
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example               # 環境変数サンプル
│   └── ocr_processor.py
│
├── azure-document-intelligence/   # Azure DI実装
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── ocr_processor.py
│
├── aoai-mistral-pdf/              # Azure OpenAI Mistral (PDF直接処理)
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── ocr_processor.py
│
├── aoai-mistral-img/              # Azure OpenAI Mistral (画像ベース処理)
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── ocr_processor.py
│
├── ms-foundry-multimodal/         # MS AI Foundry マルチモーダルモデル
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example
│   └── ocr_processor.py
│
├── sample_pdfs/                   # テスト用PDFファイル
└── README.md                      # このファイル
```

**各ディレクトリは完全に独立しており、個別にセットアップ・実行できます。**

## クイックスタート

### 1. 試したいOCRソリューションのディレクトリに移動

```bash
cd markitdown  # または docling, azure-ai-vision, azure-document-intelligence, aoai-mistral-pdf, aoai-mistral-img, ms-foundry-multimodal
```

### 2. 各ディレクトリのREADMEを参照

各ディレクトリには詳細なセットアップ手順と使い方が記載されています。

### 3. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. PDFを処理

```bash
python ocr_processor.py ../sample_pdfs/your.pdf output.txt
```

## 各ライブラリの比較

| ソリューション | 実行環境 | 認証 | 精度 | 速度 | PDF処理 | コスト | 特徴 |
|--------------|---------|------|------|------|---------|--------|------|
| **MarkItDown** | ローカル | 不要 | 中 | 速い | ライブラリ | 無料 | シンプルなテキスト抽出 |
| **Docling** | ローカル | 不要 | 高 | 中 | ライブラリ | 無料 | 構造化、Markdown出力 |
| **Azure AI Vision** | クラウド | 必要 | 高 | 速い | 画像変換 | 低価格 | OCR特化、手書き対応 |
| **Azure DI** | クラウド | 必要 | 非常に高 | 速い | 直接 | 中価格 | レイアウト、表・フォーム |
| **Azure OpenAI Mistral (PDF)** | クラウド | 必要 | 高 | 速い | **直接** | 高額 | **PDF直接処理** |
| **Azure OpenAI Mistral (Image)** | クラウド | 必要 | 高 | 遅い | 画像変換 | 高額 | 文脈理解、複雑な文書 |
| **MS Foundry Multimodal** | クラウド | 必要 | 高 | 遅い | 画像変換 | 高額 | 柔軟なモデル選択、最新モデル |

### どれを選ぶべきか？

- **無料で試したい** → MarkItDown または Docling
- **コストパフォーマンス重視** → Azure AI Vision
- **PDF直接処理したい** → Azure OpenAI Mistral (PDF) または Azure Document Intelligence
- **高精度OCRが必要** → Azure AI Vision または Azure Document Intelligence
- **表・フォーム抽出が必要** → Docling または Azure Document Intelligence
- **文脈理解が必要** → Azure OpenAI Mistral (Image) または MS Foundry Multimodal
- **最新モデルを試したい** → MS Foundry Multimodal
- **速度重視** → MarkItDown、Azure AI Vision、Azure OpenAI Mistral (PDF)

### Azure サービスの使い分け

| 用途 | 推奨サービス | 理由 |
|------|------------|------|
| シンプルなテキスト抽出 | Azure AI Vision | 低コスト、高速 |
| PDF直接処理（画像変換なし） | Azure OpenAI Mistral (PDF) | PDF直接処理、シンプル実装 |
| 表やフォームの構造抽出 | Azure Document Intelligence | レイアウト分析機能 |
| 文脈理解が必要 | Azure OpenAI Mistral (Image) | LLMによる高度な理解 |
| 最新モデルへのアクセス | MS Foundry Multimodal | GPT-4V, Phi-3-vision等から選択可能 |

## テスト用PDFの配置

テスト用のPDFファイルは `sample_pdfs/` ディレクトリに配置してください：

```bash
# PDFをsample_pdfs/に配置
cp your-document.pdf sample_pdfs/

# 各ディレクトリから参照
cd markitdown
python ocr_processor.py ../sample_pdfs/your-document.pdf output.txt
```

## トラブルシューティング

各ソリューションのトラブルシューティングについては、それぞれのディレクトリ内のREADMEを参照してください。

共通の問題：
- **pdf2image関連エラー**: `poppler-utils`のインストールが必要（Azure AI Vision、Azure OpenAI Mistral (Image)、MS Foundry Multimodal使用時）
  - **注**: Azure OpenAI Mistral (PDF)とAzure DIはPDF直接処理のため不要
- **モジュールが見つからない**: 各ディレクトリで`pip install -r requirements.txt`を実行
- **Azure認証エラー**: `.env`ファイルの設定を確認

## 参考リンク

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [Docling Documentation](https://ds4sd.github.io/docling/)
- [Azure AI Vision](https://azure.microsoft.com/ja-jp/products/ai-services/ai-vision)
- [Azure Document Intelligence](https://azure.microsoft.com/ja-jp/products/ai-services/ai-document-intelligence)
- [Mistral AI](https://mistral.ai/)
- [Azure OpenAI Service](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)
- [Microsoft AI Foundry](https://azure.microsoft.com/ja-jp/products/ai-studio/)

## このプロジェクトについて

このリポジトリは[Claude Code](https://docs.claude.com/en/docs/claude-code)を使用して作成されました。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

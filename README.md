# OCR Research

OCR（光学文字認識）技術の各種ライブラリとサービスを比較検証するためのリポジトリです。

## 概要

このプロジェクトでは、以下の4つのOCRソリューションを個別に検証できます：

1. **[MarkItDown](./markitdown/)** - Microsoftが提供するドキュメント変換ライブラリ
2. **[Docling](./docling/)** - IBM Researchが提供する高度なドキュメント処理ライブラリ
3. **[Azure Document Intelligence](./azure-document-intelligence/)** - Azureの高精度ドキュメント分析サービス
4. **[Azure OpenAI (Mistral)](./azure-openai-mistral/)** - Vision機能を使ったLLMベースのOCR

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
├── azure-document-intelligence/   # Azure DI実装
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example               # 環境変数サンプル
│   └── ocr_processor.py
│
├── azure-openai-mistral/          # Azure OpenAI実装
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
cd markitdown  # または docling, azure-document-intelligence, azure-openai-mistral
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

| ソリューション | 実行環境 | 認証 | 精度 | 速度 | コスト | 用途 |
|--------------|---------|------|------|------|--------|------|
| **MarkItDown** | ローカル | 不要 | 中 | 速い | 無料 | 基本的なテキスト抽出 |
| **Docling** | ローカル | 不要 | 高 | 中 | 無料 | 構造化されたテキスト抽出 |
| **Azure DI** | クラウド | 必要 | 非常に高 | 速い | 従量課金 | 高精度OCR、本番環境 |
| **Azure OpenAI** | クラウド | 必要 | 高 | 遅い | 高額 | 文脈理解、複雑な文書 |

### どれを選ぶべきか？

- **無料で試したい** → MarkItDown または Docling
- **高精度が必要** → Azure Document Intelligence
- **文脈理解が必要** → Azure OpenAI (Mistral)
- **テーブル抽出が必要** → Docling または Azure Document Intelligence
- **速度重視** → MarkItDown または Azure Document Intelligence

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
- **pdf2image関連エラー**: `poppler-utils`のインストールが必要（Azure OpenAI使用時）
- **モジュールが見つからない**: 各ディレクトリで`pip install -r requirements.txt`を実行
- **Azure認証エラー**: `.env`ファイルの設定を確認

## 参考リンク

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [Docling Documentation](https://ds4sd.github.io/docling/)
- [Azure Document Intelligence](https://azure.microsoft.com/ja-jp/products/ai-services/ai-document-intelligence)
- [Azure OpenAI Service](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

# Microsoft AI Foundry Multimodal OCR

Microsoft AI Foundryにデプロイされたマルチモーダルモデルを使用したPDF OCR処理。

## 特徴

- **提供元**: Microsoft AI Foundry
- **モデル**: マルチモーダルLLM（GPT-4V, Phi-3-vision, Llama-3.2-visionなど）
- **特徴**: 柔軟なモデル選択、高度な文脈理解
- **利点**: 最新モデルへのアクセス、マネージドサービス、OpenAI互換API
- **用途**: 高度な文書理解、複雑なレイアウト処理

## Microsoft AI Foundryとは

Microsoft AI Foundry（旧Azure AI Studio）は、AIモデルの発見、カスタマイズ、デプロイを統合的に行えるプラットフォームです。

### 対応モデル例
- **GPT-4 Vision** - OpenAIの最先端マルチモーダルモデル
- **Phi-3 Vision** - Microsoftの小型高性能モデル
- **Llama 3.2 Vision** - Metaのオープンソースモデル
- その他多数のマルチモーダルモデル

## セットアップ

### 1. Microsoft AI Foundryでモデルをデプロイ

1. Azure Portal で AI Foundry リソースを作成
2. モデルカタログからマルチモーダルモデルを選択
3. モデルをデプロイしてエンドポイントを取得

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
cd ms-foundry-multimodal

# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAI Foundry認証情報を設定
# MS_FOUNDRY_ENDPOINT=https://your-endpoint.inference.ai.azure.com
# MS_FOUNDRY_API_KEY=your-api-key-here
# MS_FOUNDRY_DEPLOYMENT_NAME=your-model-deployment-name
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
from ocr_processor import MSFoundryMultimodalOCR

ocr = MSFoundryMultimodalOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

print(f"Extracted {result['char_count']} characters from {len(result['pages'])} pages")
print(result['text'])
```

## 処理の流れ

1. PDFを各ページごとの画像に変換
2. 各画像をBase64エンコード
3. Microsoft AI Foundryのマルチモーダルモデルに送信
4. LLMがテキストを抽出して返却
5. 全ページのテキストを結合

## 出力形式

- ページごとに区切られたテキスト
- 高精度な文字認識
- 文脈を考慮したテキスト抽出

## 主な機能

- 複数のマルチモーダルモデルから選択可能
- 高度な文脈理解
- 複雑なレイアウトの処理
- OpenAI互換API
- マネージドサービス（スケーリング、可用性）

## 料金

モデルとリソースに応じた従量課金制です。

- モデルによって異なる料金体系
- トークンベースの課金
- 詳細は各モデルの料金ページを参照

詳細は[Azure AI Foundry pricing](https://azure.microsoft.com/ja-jp/pricing/details/ai-studio/)をご確認ください。

## 長所と短所

### 長所
- **柔軟なモデル選択**: 複数のマルチモーダルモデルから選択可能
- **最新モデルへのアクセス**: 新しいモデルが随時追加
- **マネージドサービス**: インフラ管理不要
- **OpenAI互換API**: 既存コードの移行が容易
- **高度な理解**: LLMによる文脈理解

### 短所
- コストが高い（モデルによる）
- 処理速度が遅い（ページごと処理）
- モデルの選択と設定が必要

## 他のソリューションとの比較

| ソリューション | 処理方式 | モデル選択 | コスト | 用途 |
|--------------|---------|----------|--------|------|
| **MS Foundry** | 画像ベース | 柔軟 | 高 | 高度な理解、最新モデル |
| Azure OpenAI Mistral (PDF) | PDF直接 | 固定 | 高 | PDF直接処理 |
| Azure OpenAI Mistral (Image) | 画像ベース | 固定 | 高 | 文脈理解 |
| Azure AI Vision | 画像ベース | 固定 | 低 | シンプルOCR |

## 推奨モデル

### GPT-4 Vision
- 最高精度
- 複雑な文書理解
- コスト: 高

### Phi-3 Vision
- バランス重視
- 高速処理
- コスト: 中

### Llama 3.2 Vision
- オープンソース
- カスタマイズ可能
- コスト: 低〜中

## トラブルシューティング

### エラー: "Endpoint not found"
- エンドポイントURLが正しいか確認
- AI Foundryでモデルがデプロイされているか確認

### エラー: "Invalid API key"
- `.env`ファイルのAPIキーが正しいか確認
- APIキーの有効期限を確認

### モデルが動作しない
- デプロイメント名が正しいか確認
- モデルがマルチモーダル（Vision）対応か確認

## 参考リンク

- [Microsoft AI Foundry](https://azure.microsoft.com/ja-jp/products/ai-studio/)
- [AI Foundry Documentation](https://learn.microsoft.com/ja-jp/azure/ai-studio/)
- [Model Catalog](https://learn.microsoft.com/ja-jp/azure/ai-studio/how-to/model-catalog)
- [Deploy Models](https://learn.microsoft.com/ja-jp/azure/ai-studio/how-to/deploy-models)

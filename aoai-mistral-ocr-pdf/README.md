# Mistral OCR (Azure OpenAI)

Azure OpenAIにデプロイされたMistral OCRモデルを使用したPDF OCR処理。

## 特徴

- **提供元**: Mistral AI (Azure OpenAI経由)
- **モデル**: Mistral OCR (Pixtral OCR)
- **特徴**: **PDFを直接処理可能**、画像変換不要
- **利点**: シンプルな実装、高精度OCR、構造理解
- **用途**: PDFドキュメントのテキスト抽出、ドキュメント理解

## Mistral OCR vs Azure OpenAI Vision

| 機能 | Mistral OCR | Azure OpenAI Vision |
|------|------------|---------------------|
| **PDF処理** | 直接処理可能 | 画像変換が必要 |
| **実装の複雑さ** | シンプル | やや複雑（pdf2image必要） |
| **処理速度** | 速い | 遅い（ページごと処理） |
| **精度** | 高い | 高い |
| **用途** | PDFドキュメント | 画像ベース |

**Mistral OCRを選ぶべき場合:**
- PDFを直接処理したい
- シンプルな実装を好む
- ページごとの処理が不要

**Azure OpenAI Visionを選ぶべき場合:**
- ページごとに細かく制御したい
- 画像ファイルを処理したい
- カスタムプロンプトで特定の情報を抽出

## セットアップ

### 1. Azure OpenAIでMistral OCRモデルをデプロイ

Azure Portal で Azure OpenAI Service リソースを作成し、Mistral OCRモデルをデプロイします。

### 2. 環境変数の設定

```bash
cd mistral-ocr

# .envファイルを作成
cp .env.example .env

# .envファイルを編集してAzure認証情報を設定
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-key-here
# AZURE_OPENAI_DEPLOYMENT_NAME=mistral-ocr
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方

### 基本的な使用方法

```bash
# PDFからテキストを抽出（PDF直接処理）
python ocr_processor.py ../sample_pdfs/your.pdf output.txt
```

### Pythonコードから使用

```python
from ocr_processor import MistralOCR

ocr = MistralOCR()
result = ocr.process_pdf("input.pdf", "output.txt")

if result['success']:
    print(f"Extracted {result['char_count']} characters")
    print(result['text'])
else:
    print(f"Error: {result['error']}")
```

## 処理の流れ

1. PDFファイルをBase64エンコード
2. Azure OpenAI Mistral OCR APIに送信（PDF直接）
3. 抽出されたテキストを取得
4. ファイルに保存

**画像変換不要！** PDFを直接処理できるため、`pdf2image`や`poppler`のインストールは不要です。

## 出力形式

- 全ページのテキストを統合して返却
- 高精度な文字認識結果
- ドキュメント構造を考慮したテキスト抽出

## 主な機能

- PDF直接処理（画像変換不要）
- 高精度なテキスト認識
- 複雑なレイアウトの処理
- 多言語対応
- テーブルや構造化データの理解

## 料金

Azure OpenAI Serviceの従量課金制です。

- トークンベースの課金
- 入力トークン + 出力トークンの合計

詳細は[Azure OpenAI pricing](https://azure.microsoft.com/ja-jp/pricing/details/cognitive-services/openai-service/)をご確認ください。

## 長所と短所

### 長所
- **PDF直接処理**: 画像変換が不要でシンプル
- 高精度なOCR
- ドキュメント構造の理解
- シンプルな実装（依存関係が少ない）

### 短所
- Azure OpenAI Service環境が必要
- コストがかかる
- ページごとの細かい制御は困難

## トラブルシューティング

### エラー: "Model not found"
- デプロイメント名が正しいか確認
- Azure OpenAIでMistral OCRモデルがデプロイされているか確認

### エラー: "Invalid API key"
- `.env`ファイルのAPIキーが正しいか確認
- エンドポイントURLが正しいか確認

### PDFが大きすぎる
- Mistral OCRは大きなPDFも処理できますが、トークン制限に注意
- 必要に応じて`max_tokens`を調整

## 他のソリューションとの比較

| ソリューション | PDF処理 | 依存関係 | 実装の複雑さ |
|--------------|---------|---------|------------|
| **Mistral OCR** | 直接 | 少ない | シンプル |
| Azure OpenAI Vision | 画像変換経由 | 多い | やや複雑 |
| Azure AI Vision | 画像変換経由 | 多い | やや複雑 |
| Azure DI | 直接 | 少ない | シンプル |

## 参考リンク

- [Mistral AI](https://mistral.ai/)
- [Azure OpenAI Service](https://azure.microsoft.com/ja-jp/products/ai-services/openai-service)
- [Mistral OCR Documentation](https://docs.mistral.ai/capabilities/vision/)

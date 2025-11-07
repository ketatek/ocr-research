"""
Azure Document Intelligence を使用したPDF OCR処理
Azure Document Intelligence (旧 Form Recognizer) はMicrosoftの高精度ドキュメント処理サービス
"""

import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# 環境変数を読み込み
load_dotenv()


class AzureDocumentIntelligenceOCR:
    """Azure Document Intelligence を使用したOCR処理クラス"""

    def __init__(self, endpoint: str = None, api_key: str = None):
        """
        初期化

        Args:
            endpoint: Azure Document Intelligence エンドポイント
            api_key: Azure Document Intelligence APIキー
        """
        # 環境変数から取得（引数で指定されていない場合）
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure Document Intelligence endpoint and API key are required.\n"
                "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY\n"
                "environment variables in .env file or pass them as arguments."
            )

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        print("✓ Azure Document Intelligence initialized successfully")

    def process_pdf(self, pdf_path: str, output_path: str = None, model: str = "prebuilt-read"):
        """
        PDFファイルをOCR処理

        Args:
            pdf_path: 入力PDFファイルのパス
            output_path: 出力ファイルのパス（Noneの場合は保存しない）
            model: 使用するモデル（prebuilt-read, prebuilt-layout, prebuilt-document など）

        Returns:
            変換結果を含む辞書
        """
        print(f"\n📄 Processing PDF: {pdf_path}")
        print(f"🔧 Using model: {model}")

        # PDFファイルの存在確認
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # PDFファイルを読み込み
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()

        # Document Intelligence APIを呼び出し
        print("⏳ Analyzing document...")
        poller = self.client.begin_analyze_document(
            model_id=model,
            analyze_request=pdf_content,
            content_type="application/pdf"
        )

        analysis_result = poller.result()

        # テキストを抽出
        text_parts = []
        pages_info = []

        if hasattr(analysis_result, 'pages'):
            for page_num, page in enumerate(analysis_result.pages, start=1):
                page_text = []

                if hasattr(page, 'lines'):
                    for line in page.lines:
                        page_text.append(line.content)

                page_content = '\n'.join(page_text)
                text_parts.append(f"--- Page {page_num} ---\n{page_content}")

                pages_info.append({
                    'page_number': page_num,
                    'text': page_content,
                    'line_count': len(page_text)
                })

        text_content = '\n\n'.join(text_parts)

        print(f"✓ Extracted {len(text_content)} characters from {len(pages_info)} pages")

        # 出力ファイルに保存
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"✓ Output saved to: {output_path}")

        return {
            'success': True,
            'text': text_content,
            'pages': pages_info,
            'output_path': output_path,
            'char_count': len(text_content)
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_processor.py <pdf_path> [output_path] [model]")
        print("\nModels:")
        print("  - prebuilt-read (default): 基本的なテキスト抽出")
        print("  - prebuilt-layout: レイアウト情報を含む抽出")
        print("  - prebuilt-document: ドキュメント全体の構造解析")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    model = sys.argv[3] if len(sys.argv) > 3 else "prebuilt-read"

    try:
        ocr = AzureDocumentIntelligenceOCR()
        result = ocr.process_pdf(pdf_path, output_path, model)
        print(f"\n✅ Success! Extracted {result['char_count']} characters from {len(result['pages'])} pages")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your Azure credentials:")
        print("  cp .env.example .env")
        print("  # Edit .env with your actual credentials")
        sys.exit(1)

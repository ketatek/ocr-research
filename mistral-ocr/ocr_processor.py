"""
Azure OpenAI Mistral OCR を使用したPDF OCR処理
Mistral OCRモデルはPDFを直接処理できる専用のOCRモデル
"""

import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI

# 環境変数を読み込み
load_dotenv()


class MistralOCR:
    """Azure OpenAI Mistral OCR を使用したOCR処理クラス"""

    def __init__(self,
                 endpoint: str = None,
                 api_key: str = None,
                 deployment_name: str = None,
                 api_version: str = None):
        """
        初期化

        Args:
            endpoint: Azure OpenAI エンドポイント
            api_key: Azure OpenAI APIキー
            deployment_name: デプロイメント名（Mistral OCRモデル）
            api_version: APIバージョン
        """
        # 環境変数から取得（引数で指定されていない場合）
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "mistral-ocr")
        self.api_version = api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure OpenAI endpoint and API key are required.\n"
                "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY\n"
                "environment variables in .env file or pass them as arguments."
            )

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
        print(f"✓ Azure OpenAI Mistral OCR initialized with deployment: {self.deployment_name}")

    def process_pdf(self, pdf_path: str, output_path: str = None):
        """
        PDFファイルをOCR処理（PDF直接処理）

        Args:
            pdf_path: 入力PDFファイルのパス
            output_path: 出力ファイルのパス（Noneの場合は保存しない）

        Returns:
            変換結果を含む辞書
        """
        print(f"\n📄 Processing PDF: {pdf_path}")

        # PDFファイルの存在確認
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # PDFファイルをBase64エンコード
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        print("⏳ Analyzing PDF with Mistral OCR...")

        try:
            # Mistral OCR APIを呼び出し（PDFを直接処理）
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an OCR assistant. Extract all text from the provided PDF document accurately, "
                                 "maintaining the original structure and formatting as much as possible. "
                                 "Include all text, including headers, footers, tables, and any other content."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from this PDF document."
                            },
                            {
                                "type": "document",
                                "document": {
                                    "data": pdf_base64,
                                    "format": "pdf"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=8000,
                temperature=0.0
            )

            extracted_text = response.choices[0].message.content

            print(f"✓ Extracted {len(extracted_text)} characters")

            # 出力ファイルに保存
            if output_path:
                os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"✓ Output saved to: {output_path}")

            return {
                'success': True,
                'text': extracted_text,
                'output_path': output_path,
                'char_count': len(extracted_text)
            }

        except Exception as e:
            error_msg = f"Error processing PDF with Mistral OCR: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'text': '',
                'error': error_msg
            }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_processor.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    try:
        ocr = MistralOCR()
        result = ocr.process_pdf(pdf_path, output_path)

        if result['success']:
            print(f"\n✅ Success! Extracted {result['char_count']} characters")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your Azure credentials:")
        print("  cp .env.example .env")
        print("  # Edit .env with your actual credentials")
        sys.exit(1)

"""
Microsoft AI Foundry マルチモーダルモデル を使用したPDF OCR処理
Microsoft AI Foundryにデプロイされたマルチモーダルモデル（GPT-4V, Phi-3-visionなど）を使用
"""

import os
import base64
import io
from dotenv import load_dotenv
from openai import OpenAI
from pdf2image import convert_from_path
from PIL import Image

# 環境変数を読み込み
load_dotenv()


class MSFoundryMultimodalOCR:
    """Microsoft AI Foundry マルチモーダルモデル を使用したOCR処理クラス"""

    def __init__(self,
                 endpoint: str = None,
                 api_key: str = None,
                 deployment_name: str = None):
        """
        初期化

        Args:
            endpoint: Microsoft AI Foundry エンドポイント
            api_key: Microsoft AI Foundry APIキー
            deployment_name: デプロイメント名（マルチモーダルモデル）
        """
        # 環境変数から取得（引数で指定されていない場合）
        self.endpoint = endpoint or os.getenv("MS_FOUNDRY_ENDPOINT")
        self.api_key = api_key or os.getenv("MS_FOUNDRY_API_KEY")
        self.deployment_name = deployment_name or os.getenv("MS_FOUNDRY_DEPLOYMENT_NAME")

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Microsoft AI Foundry endpoint and API key are required.\n"
                "Set MS_FOUNDRY_ENDPOINT and MS_FOUNDRY_API_KEY\n"
                "environment variables in .env file or pass them as arguments."
            )

        # OpenAI互換のクライアントを作成
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.api_key
        )
        print(f"✓ Microsoft AI Foundry initialized")
        if self.deployment_name:
            print(f"  Model: {self.deployment_name}")

    def _pdf_to_images(self, pdf_path: str):
        """
        PDFを画像に変換してBase64エンコード

        Args:
            pdf_path: PDFファイルパス

        Returns:
            Base64エンコードされた画像のリスト
        """
        print("⏳ Converting PDF to images...")

        # PDFを画像に変換
        images = convert_from_path(pdf_path)
        base64_images = []

        for i, image in enumerate(images, 1):
            # 画像をBase64エンコード
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            base64_images.append(img_str)

        print(f"✓ Converted {len(base64_images)} pages to images")
        return base64_images

    def _extract_text_from_image(self, base64_image: str, page_num: int):
        """
        画像からテキストを抽出

        Args:
            base64_image: Base64エンコードされた画像
            page_num: ページ番号

        Returns:
            抽出されたテキスト
        """
        print(f"⏳ Processing page {page_num}...")

        try:
            # マルチモーダルモデルを使用してテキスト抽出
            messages = [
                {
                    "role": "system",
                    "content": "You are an OCR assistant. Extract all text from the provided image accurately, "
                             "maintaining the original structure and formatting as much as possible. "
                             "Include all text, including headers, footers, tables, and any other content."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract all text from this document page."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]

            # デプロイメント名が指定されている場合は使用
            if self.deployment_name:
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    max_tokens=4000,
                    temperature=0.0
                )
            else:
                response = self.client.chat.completions.create(
                    messages=messages,
                    max_tokens=4000,
                    temperature=0.0
                )

            extracted_text = response.choices[0].message.content
            print(f"✓ Extracted {len(extracted_text)} characters from page {page_num}")
            return extracted_text

        except Exception as e:
            error_msg = f"Error processing page {page_num}: {str(e)}"
            print(f"⚠️  {error_msg}")
            return f"[{error_msg}]"

    def process_pdf(self, pdf_path: str, output_path: str = None):
        """
        PDFファイルをOCR処理

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

        # PDFを画像に変換
        base64_images = self._pdf_to_images(pdf_path)

        # 各ページからテキストを抽出
        page_texts = []
        for i, base64_image in enumerate(base64_images, start=1):
            page_text = self._extract_text_from_image(base64_image, i)
            page_texts.append(f"--- Page {i} ---\n{page_text}")

        # 全ページのテキストを結合
        text_content = '\n\n'.join(page_texts)

        print(f"\n✓ Total extracted: {len(text_content)} characters from {len(page_texts)} pages")

        # 出力ファイルに保存
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"✓ Output saved to: {output_path}")

        return {
            'success': True,
            'text': text_content,
            'pages': page_texts,
            'output_path': output_path,
            'char_count': len(text_content)
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_processor.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    try:
        ocr = MSFoundryMultimodalOCR()
        result = ocr.process_pdf(pdf_path, output_path)
        print(f"\n✅ Success! Extracted {result['char_count']} characters from {len(result['pages'])} pages")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your Microsoft AI Foundry credentials:")
        print("  cp .env.example .env")
        print("  # Edit .env with your actual credentials")
        sys.exit(1)

"""
Azure AI Vision を使用したPDF OCR処理
Azure AI VisionのRead APIを使用して高精度なOCR処理を実行
"""

import os
import time
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from pdf2image import convert_from_path
from PIL import Image
import io

# 環境変数を読み込み
load_dotenv()


class AzureAIVisionOCR:
    """Azure AI Vision を使用したOCR処理クラス"""

    def __init__(self, endpoint: str = None, api_key: str = None):
        """
        初期化

        Args:
            endpoint: Azure AI Vision エンドポイント
            api_key: Azure AI Vision APIキー
        """
        # 環境変数から取得（引数で指定されていない場合）
        self.endpoint = endpoint or os.getenv("AZURE_VISION_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_VISION_KEY")

        if not self.endpoint or not self.api_key:
            raise ValueError(
                "Azure AI Vision endpoint and API key are required.\n"
                "Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY\n"
                "environment variables in .env file or pass them as arguments."
            )

        self.client = ImageAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        print("✓ Azure AI Vision initialized successfully")

    def _analyze_image_bytes(self, image_bytes: bytes, page_num: int):
        """
        画像バイトからテキストを抽出

        Args:
            image_bytes: 画像のバイトデータ
            page_num: ページ番号

        Returns:
            抽出されたテキスト
        """
        print(f"⏳ Processing page {page_num}...")

        try:
            # Azure AI Vision APIを呼び出し
            result = self.client.analyze(
                image_data=image_bytes,
                visual_features=[VisualFeatures.READ]
            )

            # テキストを抽出
            text_lines = []
            if result.read is not None:
                for block in result.read.blocks:
                    for line in block.lines:
                        text_lines.append(line.text)

            extracted_text = '\n'.join(text_lines)
            print(f"✓ Extracted {len(extracted_text)} characters from page {page_num}")
            return extracted_text

        except Exception as e:
            error_msg = f"Error processing page {page_num}: {str(e)}"
            print(f"⚠️  {error_msg}")
            return f"[{error_msg}]"

    def _pdf_to_images(self, pdf_path: str):
        """
        PDFを画像に変換

        Args:
            pdf_path: PDFファイルパス

        Returns:
            画像のバイトデータのリスト
        """
        print("⏳ Converting PDF to images...")

        # PDFを画像に変換
        images = convert_from_path(pdf_path)
        image_bytes_list = []

        for i, image in enumerate(images, 1):
            # 画像をバイトデータに変換
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_bytes = buffered.getvalue()
            image_bytes_list.append(image_bytes)

        print(f"✓ Converted {len(image_bytes_list)} pages to images")
        return image_bytes_list

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
        image_bytes_list = self._pdf_to_images(pdf_path)

        # 各ページからテキストを抽出
        page_texts = []
        for i, image_bytes in enumerate(image_bytes_list, start=1):
            page_text = self._analyze_image_bytes(image_bytes, i)
            page_texts.append(f"--- Page {i} ---\n{page_text}")

            # レート制限を避けるため少し待機
            if i < len(image_bytes_list):
                time.sleep(0.5)

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
        ocr = AzureAIVisionOCR()
        result = ocr.process_pdf(pdf_path, output_path)
        print(f"\n✅ Success! Extracted {result['char_count']} characters from {len(result['pages'])} pages")
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your Azure credentials:")
        print("  cp .env.example .env")
        print("  # Edit .env with your actual credentials")
        sys.exit(1)

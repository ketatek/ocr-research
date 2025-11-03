"""
Azure OpenAI (Mistral モデル) を使用したPDF OCR処理
Vision機能を使ってPDFの各ページを画像として処理し、テキストを抽出
"""

import os
import base64
from pathlib import Path
from typing import Dict, Optional, List
from loguru import logger


class AzureOpenAIOCR:
    """Azure OpenAI (Mistral モデル) を使用したOCR処理クラス"""

    def __init__(self,
                 endpoint: Optional[str] = None,
                 api_key: Optional[str] = None,
                 deployment_name: Optional[str] = None,
                 api_version: str = "2024-02-15-preview"):
        """
        初期化

        Args:
            endpoint: Azure OpenAI エンドポイント
            api_key: Azure OpenAI APIキー
            deployment_name: デプロイメント名（Mistralモデル）
            api_version: APIバージョン
        """
        try:
            from openai import AzureOpenAI

            # 環境変数から取得（引数で指定されていない場合）
            self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
            self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
            self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "mistral")

            if not self.endpoint or not self.api_key:
                raise ValueError(
                    "Azure OpenAI endpoint and API key are required. "
                    "Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY "
                    "environment variables or pass them as arguments."
                )

            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=api_version,
                azure_endpoint=self.endpoint
            )
            logger.info(f"Azure OpenAI initialized successfully with deployment: {self.deployment_name}")

        except ImportError as e:
            logger.error(f"Failed to import OpenAI SDK: {e}")
            raise

    def _pdf_to_images(self, pdf_path: str) -> List[str]:
        """
        PDFを画像に変換してBase64エンコード

        Args:
            pdf_path: PDFファイルパス

        Returns:
            Base64エンコードされた画像のリスト
        """
        try:
            from pdf2image import convert_from_path
            from PIL import Image
            import io

            logger.info(f"Converting PDF to images: {pdf_path}")

            # PDFを画像に変換
            images = convert_from_path(pdf_path)
            base64_images = []

            for i, image in enumerate(images):
                # 画像をBase64エンコード
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                base64_images.append(img_str)

            logger.info(f"Converted {len(base64_images)} pages to images")
            return base64_images

        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            raise

    def _extract_text_from_image(self, base64_image: str, page_num: int) -> str:
        """
        画像からテキストを抽出

        Args:
            base64_image: Base64エンコードされた画像
            page_num: ページ番号

        Returns:
            抽出されたテキスト
        """
        try:
            logger.info(f"Processing page {page_num} with Azure OpenAI (Mistral)")

            # Vision APIを使用してテキスト抽出
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
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
                ],
                max_tokens=4000,
                temperature=0.0
            )

            extracted_text = response.choices[0].message.content
            return extracted_text

        except Exception as e:
            logger.error(f"Error extracting text from page {page_num}: {e}")
            return f"[Error processing page {page_num}: {str(e)}]"

    def process_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> Dict[str, any]:
        """
        PDFファイルをOCR処理

        Args:
            pdf_path: 入力PDFファイルのパス
            output_path: 出力ファイルのパス（Noneの場合は保存しない）

        Returns:
            変換結果を含む辞書
            {
                'success': bool,
                'text': str,
                'pages': List[str],
                'output_path': str or None,
                'error': str or None
            }
        """
        result = {
            'success': False,
            'text': '',
            'pages': [],
            'output_path': None,
            'error': None
        }

        try:
            logger.info(f"Processing PDF with Azure OpenAI (Mistral): {pdf_path}")

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
            result['text'] = text_content
            result['pages'] = page_texts
            result['success'] = True

            # 出力ファイルに保存
            if output_path:
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)

                result['output_path'] = output_path
                logger.info(f"Output saved to: {output_path}")

            logger.success(f"Successfully processed PDF with Azure OpenAI (Mistral)")
            logger.info(f"Extracted text length: {len(text_content)} characters")
            logger.info(f"Total pages: {len(page_texts)}")

        except Exception as e:
            logger.error(f"Error processing PDF with Azure OpenAI (Mistral): {e}")
            result['error'] = str(e)

        return result

    def process_multiple_pdfs(self, pdf_dir: str, output_dir: str) -> Dict[str, Dict]:
        """
        複数のPDFファイルを一括処理

        Args:
            pdf_dir: 入力PDFディレクトリ
            output_dir: 出力ディレクトリ

        Returns:
            各ファイルの処理結果を含む辞書
        """
        results = {}
        pdf_files = list(Path(pdf_dir).glob("*.pdf"))

        logger.info(f"Found {len(pdf_files)} PDF files in {pdf_dir}")

        for pdf_file in pdf_files:
            output_file = os.path.join(
                output_dir,
                f"{pdf_file.stem}_azure_openai.txt"
            )

            result = self.process_pdf(str(pdf_file), output_file)
            results[pdf_file.name] = result

        return results


def main():
    """テスト実行用のメイン関数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python azure_openai_ocr.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    ocr = AzureOpenAIOCR()
    result = ocr.process_pdf(pdf_path, output_path)

    if result['success']:
        print(f"Success! Text length: {len(result['text'])} characters")
        print(f"Total pages: {len(result['pages'])}")
        if result['output_path']:
            print(f"Output saved to: {result['output_path']}")
    else:
        print(f"Failed: {result['error']}")


if __name__ == "__main__":
    main()

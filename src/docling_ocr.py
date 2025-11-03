"""
Docling を使用したPDF OCR処理
DoclingはIBM Researchが提供する高度なドキュメント変換ライブラリ
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
from loguru import logger


class DoclingOCR:
    """Docling を使用したOCR処理クラス"""

    def __init__(self):
        """初期化"""
        try:
            from docling.document_converter import DocumentConverter
            self.converter = DocumentConverter()
            logger.info("Docling initialized successfully")
        except ImportError as e:
            logger.error(f"Failed to import Docling: {e}")
            raise

    def process_pdf(self, pdf_path: str, output_path: Optional[str] = None) -> Dict[str, any]:
        """
        PDFファイルをテキストに変換

        Args:
            pdf_path: 入力PDFファイルのパス
            output_path: 出力ファイルのパス（Noneの場合は保存しない）

        Returns:
            変換結果を含む辞書
            {
                'success': bool,
                'text': str,
                'markdown': str,
                'output_path': str or None,
                'error': str or None
            }
        """
        result = {
            'success': False,
            'text': '',
            'markdown': '',
            'output_path': None,
            'error': None
        }

        try:
            logger.info(f"Processing PDF with Docling: {pdf_path}")

            # PDFファイルの存在確認
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            # PDFを変換
            conversion_result = self.converter.convert(pdf_path)

            # テキストとMarkdownを取得
            text_content = conversion_result.document.export_to_text()
            markdown_content = conversion_result.document.export_to_markdown()

            result['text'] = text_content
            result['markdown'] = markdown_content
            result['success'] = True

            # 出力ファイルに保存
            if output_path:
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                # テキストファイルとして保存
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)

                # Markdownファイルも保存
                md_output_path = output_path.replace('.txt', '.md')
                with open(md_output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                result['output_path'] = output_path
                logger.info(f"Text output saved to: {output_path}")
                logger.info(f"Markdown output saved to: {md_output_path}")

            logger.success(f"Successfully processed PDF with Docling")
            logger.info(f"Extracted text length: {len(text_content)} characters")

        except Exception as e:
            logger.error(f"Error processing PDF with Docling: {e}")
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
                f"{pdf_file.stem}_docling.txt"
            )

            result = self.process_pdf(str(pdf_file), output_file)
            results[pdf_file.name] = result

        return results

    def get_document_structure(self, pdf_path: str) -> Dict[str, any]:
        """
        ドキュメントの構造情報を取得

        Args:
            pdf_path: 入力PDFファイルのパス

        Returns:
            ドキュメント構造情報
        """
        try:
            logger.info(f"Extracting document structure: {pdf_path}")

            conversion_result = self.converter.convert(pdf_path)
            doc = conversion_result.document

            structure = {
                'page_count': len(doc.pages) if hasattr(doc, 'pages') else 0,
                'has_tables': False,
                'has_images': False,
                'metadata': {}
            }

            # メタデータの取得
            if hasattr(doc, 'metadata'):
                structure['metadata'] = doc.metadata

            logger.success("Document structure extracted successfully")
            return structure

        except Exception as e:
            logger.error(f"Error extracting document structure: {e}")
            return {'error': str(e)}


def main():
    """テスト実行用のメイン関数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python docling_ocr.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    ocr = DoclingOCR()
    result = ocr.process_pdf(pdf_path, output_path)

    if result['success']:
        print(f"Success! Text length: {len(result['text'])} characters")
        print(f"Markdown length: {len(result['markdown'])} characters")
        if result['output_path']:
            print(f"Output saved to: {result['output_path']}")
    else:
        print(f"Failed: {result['error']}")


if __name__ == "__main__":
    main()

"""
Docling を使用したPDF OCR処理
DoclingはIBM Researchが提供する高度なドキュメント変換ライブラリ
"""

import os
from pathlib import Path
from docling.document_converter import DocumentConverter


class DoclingOCR:
    """Docling を使用したOCR処理クラス"""

    def __init__(self):
        """初期化"""
        self.converter = DocumentConverter()
        print("✓ Docling initialized successfully")

    def process_pdf(self, pdf_path: str, output_path: str = None):
        """
        PDFファイルをテキストに変換

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

        # PDFを変換
        conversion_result = self.converter.convert(pdf_path)

        # テキストとMarkdownを取得
        text_content = conversion_result.document.export_to_text()
        markdown_content = conversion_result.document.export_to_markdown()

        print(f"✓ Extracted {len(text_content)} characters (text)")
        print(f"✓ Generated {len(markdown_content)} characters (markdown)")

        # 出力ファイルに保存
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

            # テキストファイルとして保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text_content)
            print(f"✓ Text output saved to: {output_path}")

            # Markdownファイルも保存
            md_output_path = output_path.replace('.txt', '.md')
            with open(md_output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✓ Markdown output saved to: {md_output_path}")

        return {
            'success': True,
            'text': text_content,
            'markdown': markdown_content,
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

    ocr = DoclingOCR()
    result = ocr.process_pdf(pdf_path, output_path)

    print(f"\n✅ Success! Extracted {result['char_count']} characters")

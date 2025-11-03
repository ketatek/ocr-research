"""
Azure Document Intelligence を使用したPDF OCR処理
Azure Document Intelligence (旧 Form Recognizer) はMicrosoftの高精度ドキュメント処理サービス
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
from loguru import logger


class AzureDocumentIntelligenceOCR:
    """Azure Document Intelligence を使用したOCR処理クラス"""

    def __init__(self, endpoint: Optional[str] = None, api_key: Optional[str] = None):
        """
        初期化

        Args:
            endpoint: Azure Document Intelligence エンドポイント
            api_key: Azure Document Intelligence APIキー
        """
        try:
            from azure.ai.documentintelligence import DocumentIntelligenceClient
            from azure.core.credentials import AzureKeyCredential

            # 環境変数から取得（引数で指定されていない場合）
            self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
            self.api_key = api_key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

            if not self.endpoint or not self.api_key:
                raise ValueError(
                    "Azure Document Intelligence endpoint and API key are required. "
                    "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY "
                    "environment variables or pass them as arguments."
                )

            self.client = DocumentIntelligenceClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.api_key)
            )
            logger.info("Azure Document Intelligence initialized successfully")

        except ImportError as e:
            logger.error(f"Failed to import Azure Document Intelligence SDK: {e}")
            raise

    def process_pdf(self, pdf_path: str, output_path: Optional[str] = None,
                   model: str = "prebuilt-read") -> Dict[str, any]:
        """
        PDFファイルをOCR処理

        Args:
            pdf_path: 入力PDFファイルのパス
            output_path: 出力ファイルのパス（Noneの場合は保存しない）
            model: 使用するモデル（prebuilt-read, prebuilt-layout, prebuilt-document など）

        Returns:
            変換結果を含む辞書
            {
                'success': bool,
                'text': str,
                'pages': List[Dict],
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
            logger.info(f"Processing PDF with Azure Document Intelligence: {pdf_path}")
            logger.info(f"Using model: {model}")

            # PDFファイルの存在確認
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            # PDFファイルを読み込み
            with open(pdf_path, "rb") as f:
                pdf_content = f.read()

            # Document Intelligence APIを呼び出し
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
            result['text'] = text_content
            result['pages'] = pages_info
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

            logger.success(f"Successfully processed PDF with Azure Document Intelligence")
            logger.info(f"Extracted text length: {len(text_content)} characters")
            logger.info(f"Total pages: {len(pages_info)}")

        except Exception as e:
            logger.error(f"Error processing PDF with Azure Document Intelligence: {e}")
            result['error'] = str(e)

        return result

    def process_multiple_pdfs(self, pdf_dir: str, output_dir: str,
                            model: str = "prebuilt-read") -> Dict[str, Dict]:
        """
        複数のPDFファイルを一括処理

        Args:
            pdf_dir: 入力PDFディレクトリ
            output_dir: 出力ディレクトリ
            model: 使用するモデル

        Returns:
            各ファイルの処理結果を含む辞書
        """
        results = {}
        pdf_files = list(Path(pdf_dir).glob("*.pdf"))

        logger.info(f"Found {len(pdf_files)} PDF files in {pdf_dir}")

        for pdf_file in pdf_files:
            output_file = os.path.join(
                output_dir,
                f"{pdf_file.stem}_azure_di.txt"
            )

            result = self.process_pdf(str(pdf_file), output_file, model)
            results[pdf_file.name] = result

        return results

    def extract_tables(self, pdf_path: str) -> Dict[str, any]:
        """
        PDFから表を抽出

        Args:
            pdf_path: 入力PDFファイルのパス

        Returns:
            表データを含む辞書
        """
        try:
            logger.info(f"Extracting tables from PDF: {pdf_path}")

            with open(pdf_path, "rb") as f:
                pdf_content = f.read()

            poller = self.client.begin_analyze_document(
                model_id="prebuilt-layout",
                analyze_request=pdf_content,
                content_type="application/pdf"
            )

            analysis_result = poller.result()
            tables = []

            if hasattr(analysis_result, 'tables'):
                for table_idx, table in enumerate(analysis_result.tables):
                    table_data = {
                        'table_id': table_idx,
                        'row_count': table.row_count,
                        'column_count': table.column_count,
                        'cells': []
                    }

                    if hasattr(table, 'cells'):
                        for cell in table.cells:
                            table_data['cells'].append({
                                'row_index': cell.row_index,
                                'column_index': cell.column_index,
                                'content': cell.content
                            })

                    tables.append(table_data)

            logger.success(f"Extracted {len(tables)} tables")
            return {'success': True, 'tables': tables}

        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
            return {'success': False, 'error': str(e)}


def main():
    """テスト実行用のメイン関数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python azure_document_intelligence.py <pdf_path> [output_path]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    ocr = AzureDocumentIntelligenceOCR()
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

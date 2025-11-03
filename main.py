"""
OCR Research - メインスクリプト
各種OCRライブラリとサービスを比較検証
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict
from loguru import logger
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ログ設定
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/ocr_research_{time}.log", rotation="1 day", level="DEBUG")


def setup_args():
    """コマンドライン引数の設定"""
    parser = argparse.ArgumentParser(description="OCR Research - 各種OCRライブラリ/サービスの検証")

    parser.add_argument("pdf_path", help="入力PDFファイルまたはディレクトリのパス")
    parser.add_argument("-o", "--output", default="output", help="出力ディレクトリ（デフォルト: output）")
    parser.add_argument("-m", "--methods", nargs="+",
                       choices=["markitdown", "docling", "azure_di", "azure_openai", "all"],
                       default=["all"],
                       help="使用するOCR方法（デフォルト: all）")
    parser.add_argument("--compare", action="store_true",
                       help="すべての方法で処理して結果を比較")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="詳細ログを表示")

    return parser.parse_args()


def process_with_markitdown(pdf_path: str, output_dir: str) -> Dict:
    """MarkItDownで処理"""
    try:
        from src.markitdown_ocr import MarkItDownOCR
        logger.info("Processing with MarkItDown...")

        ocr = MarkItDownOCR()
        output_path = os.path.join(output_dir, f"{Path(pdf_path).stem}_markitdown.txt")
        result = ocr.process_pdf(pdf_path, output_path)

        return result
    except Exception as e:
        logger.error(f"MarkItDown processing failed: {e}")
        return {'success': False, 'error': str(e)}


def process_with_docling(pdf_path: str, output_dir: str) -> Dict:
    """Doclingで処理"""
    try:
        from src.docling_ocr import DoclingOCR
        logger.info("Processing with Docling...")

        ocr = DoclingOCR()
        output_path = os.path.join(output_dir, f"{Path(pdf_path).stem}_docling.txt")
        result = ocr.process_pdf(pdf_path, output_path)

        return result
    except Exception as e:
        logger.error(f"Docling processing failed: {e}")
        return {'success': False, 'error': str(e)}


def process_with_azure_di(pdf_path: str, output_dir: str) -> Dict:
    """Azure Document Intelligenceで処理"""
    try:
        from src.azure_document_intelligence import AzureDocumentIntelligenceOCR
        logger.info("Processing with Azure Document Intelligence...")

        ocr = AzureDocumentIntelligenceOCR()
        output_path = os.path.join(output_dir, f"{Path(pdf_path).stem}_azure_di.txt")
        result = ocr.process_pdf(pdf_path, output_path)

        return result
    except Exception as e:
        logger.error(f"Azure Document Intelligence processing failed: {e}")
        return {'success': False, 'error': str(e)}


def process_with_azure_openai(pdf_path: str, output_dir: str) -> Dict:
    """Azure OpenAI (Mistral)で処理"""
    try:
        from src.azure_openai_ocr import AzureOpenAIOCR
        logger.info("Processing with Azure OpenAI (Mistral)...")

        ocr = AzureOpenAIOCR()
        output_path = os.path.join(output_dir, f"{Path(pdf_path).stem}_azure_openai.txt")
        result = ocr.process_pdf(pdf_path, output_path)

        return result
    except Exception as e:
        logger.error(f"Azure OpenAI processing failed: {e}")
        return {'success': False, 'error': str(e)}


def compare_results(results: Dict[str, Dict], output_dir: str):
    """結果を比較してレポートを作成"""
    logger.info("Generating comparison report...")

    report_lines = [
        "=" * 80,
        "OCR 処理結果 比較レポート",
        "=" * 80,
        ""
    ]

    for method, result in results.items():
        report_lines.extend([
            f"\n## {method}",
            "-" * 80,
            f"処理結果: {'成功' if result.get('success') else '失敗'}",
        ])

        if result.get('success'):
            text_length = len(result.get('text', ''))
            report_lines.append(f"抽出文字数: {text_length}")
            if result.get('output_path'):
                report_lines.append(f"出力ファイル: {result['output_path']}")
        else:
            report_lines.append(f"エラー: {result.get('error', 'Unknown error')}")

    # レポートを保存
    report_path = os.path.join(output_dir, "comparison_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    logger.success(f"Comparison report saved to: {report_path}")

    # コンソールにも出力
    print('\n'.join(report_lines))


def main():
    """メイン処理"""
    args = setup_args()

    # 詳細ログ設定
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    # 入力ファイルの確認
    pdf_path = args.pdf_path
    if not os.path.exists(pdf_path):
        logger.error(f"File not found: {pdf_path}")
        sys.exit(1)

    # 出力ディレクトリの作成
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    logger.info(f"Input PDF: {pdf_path}")
    logger.info(f"Output directory: {output_dir}")

    # 処理する方法を決定
    methods = args.methods
    if "all" in methods:
        methods = ["markitdown", "docling", "azure_di", "azure_openai"]

    logger.info(f"Processing methods: {', '.join(methods)}")

    # 各方法で処理
    results = {}

    if "markitdown" in methods:
        results["MarkItDown"] = process_with_markitdown(pdf_path, output_dir)

    if "docling" in methods:
        results["Docling"] = process_with_docling(pdf_path, output_dir)

    if "azure_di" in methods:
        results["Azure Document Intelligence"] = process_with_azure_di(pdf_path, output_dir)

    if "azure_openai" in methods:
        results["Azure OpenAI (Mistral)"] = process_with_azure_openai(pdf_path, output_dir)

    # 比較モードまたは複数の方法を使用した場合はレポート作成
    if args.compare or len(results) > 1:
        compare_results(results, output_dir)

    logger.success("All processing completed!")


if __name__ == "__main__":
    main()

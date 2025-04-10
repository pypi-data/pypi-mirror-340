"""
pdfplucker - Ferramenta para extração e processamento de documentos PDF
"""

__version__ = "0.1.1"

from pdfplucker.processor import process_batch, process_pdf, create_converter
from pdfplucker.utils import ensure_path
__all__ = [
    "process_batch", 
    "process_pdf", 
    "create_converter",
    "ensure_path",
]
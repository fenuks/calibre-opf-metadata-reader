from pathlib import Path

from calibre.customize import MetadataReaderPlugin
from calibre.ebooks.metadata.book.base import Metadata
from calibre.ebooks.metadata.opf import get_metadata as opf_metadata
from calibre.ebooks.metadata.pdf import get_metadata as pdf_metadata


class OpfMetadataReader(MetadataReaderPlugin):
    """
    Reads metadata from OPF.
    """

    name = "OPF Metadata reader"
    description = "Reads file metadata stored alongside the ebook in the OPF file"
    version = (0, 0, 1)
    author = "fenuks"

    file_types = set(["pdf"])

    def get_metadata(self, stream, _type):
        opf = Path(stream.name).with_suffix(".opf")
        if not opf.is_file():
            opf = opf.with_name("metadata.opf")
        if not opf.is_file():
            return pdf_metadata(stream)

        return metadata(stream, opf)


def metadata(pdf, opf: Path) -> Metadata:
    with opf.open("r") as fp:
        mi = opf_metadata(fp)[0]
        if getattr(mi, "cover_data", None) in ((None, None), None):
            pdf_mi = pdf_metadata(pdf)
            mi.cover_data = pdf_mi.cover_data

        return mi

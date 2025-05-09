from base64 import b64decode
from dataclasses import dataclass

from parsimonious.nodes import NodeVisitor


@dataclass
class ImageMetadata:
    width: int
    height: int
    size: int


@dataclass
class PNGImage:
    header: ImageMetadata
    payload: bytes


class ThumbnailDecoder(NodeVisitor):
    def visit_Document(self, _, visited_children) -> list[PNGImage]:
        thumbnails = visited_children

        assert isinstance(thumbnails, list)
        assert isinstance(thumbnails[0], PNGImage)
        return thumbnails

    def visit_Thumbnail(self, _, visited_children) -> PNGImage:
        header, chunks, _ = visited_children

        assert isinstance(chunks, list)
        encoded = "".join(chunks)
        return PNGImage(header, b64decode(encoded))

    def visit_Header(self, _, visited_children) -> ImageMetadata:
        _, w, _, h, _, s, _ = visited_children
        return ImageMetadata(w, h, s)

    def visit_Payload(self, _, visited_children) -> str:
        _, chunk, _ = visited_children

        return chunk.text

    def visit_Integer(self, node, _) -> int:
        return int(node.text)

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node

from .oxml.textbox import GroupBaseOxmlElement
from .shared import Parented
from .text.paragraph import Paragraph


class TextboxContent(Parented):
    """
    Proxy class for a WordprocessingML ``<w:txbxContent>`` element.
    """
    def __init__(self, txbxContent, parent):
        super(TextboxContent, self).__init__(parent)
        self._element = self._txbxContent = txbxContent

    @property
    def paragraphs(self):
        """
        |Paragraph| instance containing the sequence of paragraphs in this textbox.
        """
        return [Paragraph(p, self) for p in self._txbxContent.p_lst]

    @property
    def off_x(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.off_x
        return 0

    @property
    def off_y(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.off_y
        return 0

    @property
    def width(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.width
        return self.part.document.sections[0].page_width.pt

    @property
    def height(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.height
        return 0

    @property
    def relative_from(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.shape.mso_position_vertical_relative
        else:
            return "paragraph"

    @property
    def fillcolor(self):
        if isinstance(self._txbxContent.shape, GroupBaseOxmlElement):
            return self._txbxContent.shape.fillcolor
        return None
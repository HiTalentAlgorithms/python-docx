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
        return self._txbxContent.off_x

    @property
    def off_y(self):
        return self._txbxContent.off_y

    @property
    def width(self):
        return self._txbxContent.width

    @property
    def height(self):
        return self._txbxContent.height

    @property
    def relative_from(self):
        return self._txbxContent.shape.mso_position_vertical_relative

    @property
    def fillcolor(self):
        return self._txbxContent.shape.fillcolor
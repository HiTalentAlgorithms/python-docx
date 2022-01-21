from .oxml import CT_Textbox, CT_WpsTxbx, nsmap
from .section import Section
from .shared import lazyproperty, Parented
from .textbox import TextboxContent


class PictureShape(Parented):
    """
    Proxy for an ``<pic:pic>`` element
    """

    def __init__(self, pic, parent):
        super(PictureShape, self).__init__(parent)
        self._element = self._pic = pic

    @property
    def rId(self):
        return self._pic.blipFill.blip.embed

    @property
    def has_wrap(self):
        if hasattr(self.parent,'has_wrap'):
            return self.parent.has_wrap
        return None

    @property
    def parent(self):
        return self._pic.parent

    @lazyproperty
    def parent_section(self):
        parent = self._pic.getparent()
        while parent is not None:
            if isinstance(parent, CT_Textbox):
                return TextboxContent(parent.txbxContent, self._parent)
            elif isinstance(parent, CT_WpsTxbx):
                return None
            else:
                sectPr = parent.find('.//w:sectPr', nsmap)
                if sectPr is not None:
                    return Section(sectPr, self._parent)
            parent = parent.getparent()
        return None

    @lazyproperty
    def off_x(self):
        off_x = self._pic.spPr.ox.pt + self._pic.parent_off_x.pt
        if isinstance(self.parent_section, TextboxContent):
            off_x += self.parent_section.off_x
        return off_x

    @lazyproperty
    def off_y(self):
        off_y = self._pic.spPr.ox.pt + self._pic.parent_off_y.pt
        if isinstance(self.parent_section, TextboxContent):
            off_y += self.parent_section.off_y
        return off_y

    @lazyproperty
    def width(self):
        return self._pic.spPr.cx.pt

    @lazyproperty
    def height(self):
        return self._pic.spPr.cy.pt

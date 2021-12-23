from .simpletypes import XsdString, XsdBoolean, ST_Styles, ST_CoordSize
from .xmlchemy import BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrOne, ZeroOrMore, \
    OptionalAttribute
from ..shared import Emu, lazyproperty


class CT_AlternateContent(BaseOxmlElement):
    """
    Used for ``mc:AlternateContent``; To process the text box
    """
    choice = OneAndOnlyOne('mc:Choice')
    fallback = OneAndOnlyOne('mc:Fallback')

    @property
    def _anchor(self):
        return self.choice.drawing.anchor

    @property
    def offset_x_type(self):
        if self._anchor.is_simplePos:
            return "page"
        return self._anchor.positionH.relativeFrom

    @property
    def offset_y_type(self):
        if self._anchor.is_simplePos:
            return "page"
        return self._anchor.positionV.relativeFrom

    @property
    def offset_x(self):
        if self._anchor.is_simplePos:
            return Emu(self._anchor.simplePos.attrib.get('x'))
        return self._anchor.positionH.value

    @property
    def offset_y(self):
        if self._anchor.is_simplePos:
            return Emu(self._anchor.simplePos.attrib.get('y'))
        return self._anchor.positionV.value


class CT_AC_Choice(BaseOxmlElement):
    """
    Used for ``mc:Choice``
    """
    drawing = OneAndOnlyOne('w:drawing')


class CT_Drawing(BaseOxmlElement):
    """
    Used for ``w:drawing``
    """
    anchor = OneAndOnlyOne('wp:anchor')


class CT_Anchor(BaseOxmlElement):
    """
    Used for ``wp:anchor``
    """
    is_simplePos = RequiredAttribute('simplePos', XsdBoolean)
    positionH = ZeroOrOne('wp:positionH')
    positionV = ZeroOrOne('wp:positionV')
    simplePos = ZeroOrOne('wp:simplePos')
    graphic = OneAndOnlyOne('a:graphic')


class CT_PositionH(BaseOxmlElement):
    """
    Used for ``wp:positionH``
    """
    relativeFrom = RequiredAttribute('relativeFrom', XsdString)
    posOffset = OneAndOnlyOne('wp:posOffset')

    @property
    def value(self):
        return Emu(self.posOffset.text)


class CT_PositionV(BaseOxmlElement):
    """
    Used for ``wp:positionV``
    """
    relativeFrom = RequiredAttribute('relativeFrom', XsdString)
    posOffset = OneAndOnlyOne('wp:posOffset')

    @property
    def value(self):
        return Emu(self.posOffset.text)


class CT_AC_Fallback(BaseOxmlElement):
    """
    Used for ``mc:Fallback``
    """
    pick = OneAndOnlyOne('w:pict')


class CT_Pick(BaseOxmlElement):
    """
    Used for ``w:pict``
    """
    group = ZeroOrOne('v:group')
    shape = ZeroOrOne('v:shape')


class GroupBaseOxmlElement(BaseOxmlElement):
    @property
    def parent(self):
        return self.getparent()

    @lazyproperty
    def position(self):
        if isinstance(self.parent, self.__class__):
            return self.stype.get('position') or self.parent.position
        return self.style.get('position') or 'absolute'

    @lazyproperty
    def mso_position_vertical_relative(self):
        # Vertical distance relative position
        if isinstance(self.parent, self.__class__):
            return self.stype.get('mso_position_vertical_relative') or self.parent.mso_position_vertical_relative
        return self.style.get('mso_position_vertical_relative') or 'page'

    def _get_width_value(self, key):
        if value := self.style.get(key):
            if value.endswith('pt'):
                return float(value[:-2])
            else:
                if isinstance(self.parent, self.__class__):
                    return float(value) * getattr(self.parent, key) / self.parent.coord_size[0]
                else:
                    return 0
        else:
            return 0

    def _get_height_value(self, key):
        if value := self.style.get(key):
            if value.endswith('pt'):
                return float(value[:-2])
            else:
                if isinstance(self.parent, self.__class__):
                    return float(value) * getattr(self.parent, key) / self.parent.coord_size[1]
                else:
                    return 0
        else:
            return 0

    @lazyproperty
    def width(self):
        return self._get_width_value('width')

    @lazyproperty
    def height(self):
        return self._get_height_value('height')

    @lazyproperty
    def left(self):
        return self._get_width_value('left')

    @lazyproperty
    def top(self):
        return self._get_height_value('top')

    @lazyproperty
    def margin_left(self):
        return self._get_width_value('margin_left')

    @lazyproperty
    def margin_top(self):
        return self._get_height_value('margin_top')

    @lazyproperty
    def offset_x(self):
        if isinstance(self.parent, self.__class__):
            return self.left + self.parent.offset_x + self.parent.margin_left
        return self.left

    @lazyproperty
    def offset_y(self):
        if isinstance(self.parent, self.__class__):
            return self.top + self.parent.offset_y + self.parent.margin_top
        return self.top


class CT_Group(GroupBaseOxmlElement):
    """
    Used for ``v:group``
    """
    style = RequiredAttribute('style', ST_Styles)
    coord_size = OptionalAttribute('coordsize', ST_CoordSize)
    group = ZeroOrMore('v:group')
    shape = ZeroOrMore('v:shape')


class CT_Shape(GroupBaseOxmlElement):
    """
    Used for ``v:shape``
    """
    style = RequiredAttribute('style', ST_Styles)
    coord_size = OptionalAttribute('coordsize', ST_CoordSize)
    textbox = ZeroOrOne('v:textbox')

class CT_Textbox(BaseOxmlElement):
    """
    Used for ``v:textbox``
    """
    txbxContent = OneAndOnlyOne('w:txbxContent')

class CT_TxbxContent(BaseOxmlElement):
    """
    Used for ``v:txbxContent``
    """
    p = ZeroOrMore('w:p')


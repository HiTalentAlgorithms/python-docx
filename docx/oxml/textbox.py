from .simpletypes import XsdString, XsdBoolean, ST_Styles, ST_CoordSize, ST_CoordOrigin, ST_String
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



class CT_WpsTxbx(BaseOxmlElement):
    """
    Used for ``wps:txbx``
    """
    txbxContent = OneAndOnlyOne('w:txbxContent')


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
    rect = ZeroOrOne('v:rect')


class GroupBaseOxmlElement(BaseOxmlElement):
    style = RequiredAttribute('style', ST_Styles)
    coord_size = OptionalAttribute('coordsize', ST_CoordSize)
    coord_origin = OptionalAttribute('coordorigin', ST_CoordOrigin)
    fillcolor = OptionalAttribute('fillcolor', ST_String)

    @lazyproperty
    def parent(self):
        return self.getparent()

    @lazyproperty
    def width_unit(self):
        if not self.coord_size:
            return 12700
        if self.coord_origin:
            return self.coord_origin[0] + self.coord_size[0]
        return self.coord_size[0]

    @lazyproperty
    def height_unit(self):
        if not self.coord_size:
            return 12700
        if self.coord_origin:
            return self.coord_origin[1] + self.coord_size[1]
        return self.coord_size[1]

    @lazyproperty
    def position(self):
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.stype.get('position') or self.parent.position
        return self.style.get('position') or 'absolute'

    @lazyproperty
    def mso_position_vertical_relative(self):
        # Vertical distance relative position
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.style.get('mso_position_vertical_relative') or self.style.get('mso_height_relative') or \
                   self.parent.mso_position_vertical_relative
        return self.style.get('mso_position_vertical_relative') or self.style.get('mso_height_relative')

    def _get_width_value(self, key):
        if value := self.style.get(key):
            if value.endswith('pt'):
                return float(value[:-2])
            else:
                if isinstance(self.parent, GroupBaseOxmlElement):
                    return float(value) * self.parent.width / self.parent.width_unit
                else:
                    return 0
        else:
            return 0

    def _get_height_value(self, key):
        if value := self.style.get(key):
            if value.endswith('pt'):
                return float(value[:-2])
            else:
                if isinstance(self.parent, GroupBaseOxmlElement):
                    return float(value) * self.parent.height / self.parent.height_unit
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
        position_horizontal = self.style.get('mso_position_horizontal')
        if position_horizontal and position_horizontal != 'absolute':
            return 0
        return self._get_width_value('margin_left')

    @lazyproperty
    def margin_top(self):
        position_vertical = self.style.get('mso_position_vertical')
        if position_vertical and position_vertical != 'absolute':
            return 0
        return self._get_height_value('margin_top')

    @lazyproperty
    def off_x(self):
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.left + self.parent.off_x + self.parent.margin_left
        return self.left

    @lazyproperty
    def off_y(self):
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.top + self.parent.off_y + self.parent.margin_top
        return self.top


class CT_Group(GroupBaseOxmlElement):
    """
    Used for ``v:group``
    """
    group = ZeroOrMore('v:group')
    shape = ZeroOrMore('v:shape')
    rect = ZeroOrMore('v:rect')


class CT_Rect(GroupBaseOxmlElement):
    """
    Used for ``v:rect``
    """
    textbox = ZeroOrOne('v:textbox')


class CT_Shape(GroupBaseOxmlElement):
    """
    Used for ``v:shape``
    """
    textbox = ZeroOrOne('v:textbox')


class CT_Textbox(BaseOxmlElement):
    """
    Used for ``v:textbox``
    """
    txbxContent = OneAndOnlyOne('w:txbxContent')


class CT_TxbxContent(BaseOxmlElement):
    """
    Used for ``w:txbxContent``
    """
    p = ZeroOrMore('w:p')

    @lazyproperty
    def shape(self):
        return self.getparent().getparent()

    @lazyproperty
    def off_x(self):
        return self.shape.off_x + self.shape.margin_left

    @lazyproperty
    def off_y(self):
        return self.shape.off_y + self.shape.margin_top

    @lazyproperty
    def width(self):
        return self.shape.width

    @lazyproperty
    def height(self):
        return self.shape.height

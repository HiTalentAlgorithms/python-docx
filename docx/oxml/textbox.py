from . import CT_Anchor
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
    oval = ZeroOrOne('v:oval')


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
    def alternate(self):
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CT_AlternateContent):
                return parent
            parent = parent.getparent()
        return None

    @lazyproperty
    def anchor(self):
        parent = self.parent
        while parent is not None:
            if isinstance(parent, CT_Anchor):
                return parent
            parent = parent.getparent()
        return None

    @lazyproperty
    def has_wrap(self):
        if self.anchor is not None:
            try:
                return self.anchor.has_wrap
            except:
                return None
        return None

    @lazyproperty
    def drawing_vertical_relative_from(self):
        if self.anchor is not None:
            try:
                return self.anchor.positionV.relativeFrom
            except:
                return None
        return None

    @lazyproperty
    def drawing_horizontal_relative_from(self):
        if self.anchor is not None:
            try:
                return self.anchor.positionH.relativeFrom
            except:
                return None
        return None

    @lazyproperty
    def mso_position_vertical_relative(self):
        # Vertical distance relative position
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.style.get('mso_position_vertical_relative') or self.drawing_vertical_relative_from or \
                   self.parent.mso_position_vertical_relative
        return self.style.get('mso_position_vertical_relative') or self.drawing_vertical_relative_from

    @lazyproperty
    def mso_position_horizontal_relative(self):
        # Vertical distance relative position
        if isinstance(self.parent, GroupBaseOxmlElement):
            return self.style.get('mso_position_horizontal_relative') or self.drawing_horizontal_relative_from or \
                   self.parent.mso_position_horizontal_relative
        return self.style.get('mso_position_horizontal_relative') or self.drawing_horizontal_relative_from

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
    oval = ZeroOrOne('v:oval')


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


class CT_Oval(GroupBaseOxmlElement):
    """
    Used for ``v:oval``
    """
    textbox = ZeroOrOne('v:textbox')
    fill = ZeroOrOne('v:fill')


class CT_Fill(BaseOxmlElement):
    """
    Used for ``v:fill``
    """
    rId = OptionalAttribute('r:id', XsdString)
    type = OptionalAttribute('type', XsdString)


class CT_Roundrect(GroupBaseOxmlElement):
    """
    Used for ``v:roundrect``
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
        parent = self.getparent().getparent()
        if parent is not None and parent.tag.endswith('wsp'):
            return parent.getparent().getparent().getparent()
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

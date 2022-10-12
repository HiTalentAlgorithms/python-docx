from docx.shared import Parented


class Rect(Parented):
    """
    Proxy class for a WordprocessingML ``<v:rect>`` element.
    """
    def __init__(self, rect, parent):
        super(Rect, self).__init__(parent)
        self._element = self._rect = rect

    @property
    def has_warp(self):
        return self._rect.has_wrap

    @property
    def off_x(self):
        return self._rect.off_x

    @property
    def off_y(self):
        return self._rect.off_y

    @property
    def margin_left(self):
        return self._rect.margin_left

    @property
    def margin_top(self):
        return self._rect.margin_top

    @property
    def width(self):
        return self._rect.width

    @property
    def height(self):
        return self._rect.height

    @property
    def vertical_relative_from(self):
        return self._rect.mso_position_vertical_relative

    @property
    def horizontal_relative_from(self):
        return self._rect.mso_position_horizontal_relative

    @property
    def z_index(self):
        value = self._rect.z_index
        if value is not None:
            return float(value)
        return -1

    @property
    def fillcolor(self):
        return self._rect.fillcolor
# encoding: utf-8

"""
|NumberingPart| and closely related objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..opc.part import XmlPart
from ..shared import lazyproperty
from ..text.parfmt import ParagraphFormat


class NumberingPart(XmlPart):
    """
    Proxy for the numbering.xml part containing numbering definitions for
    a document or glossary.
    """
    @classmethod
    def new(cls):
        """
        Return newly created empty numbering part, containing only the root
        ``<w:numbering>`` element.
        """
        raise NotImplementedError

    @lazyproperty
    def numbering_definitions(self):
        """
        The |_NumberingDefinitions| instance containing the numbering
        definitions (<w:num> element proxies) for this numbering part.
        """
        return _NumberingDefinitions(self._element)

    @lazyproperty
    def numbering_map(self):
        numbering_map = {}
        abstract_nums = {}
        for abstract_num in self.element.abstractNum_lst:
            abstract_nums[abstract_num.abstractNumId] = abstract_num
        for num in self.element.num_lst:
            abstract_num = abstract_nums.get(num.abstractNumId.val)
            if abstract_num is not None:
                numbering_map[num.numId] = abstract_num
        return numbering_map

    def get_lvl(self, numPr):
        numbering = self.numbering_map.get(numPr.numId)
        if numbering is not None:
            lvl_ele = numbering.get_lvl(numPr.ilvl)
            if lvl_ele is not None:
                return AbstractNumberingLvl(lvl_ele)
        return None


class AbstractNumberingLvl:
    """
    Proxy for the w:lvl.
    """
    def __init__(self, lvl_elm):
        self._lvl_elm = lvl_elm
        self._index = int(lvl_elm.start.val if lvl_elm.start is not None else 1) - 1

    def is_serial(self):
        if self._lvl_elm.numFmt.val == 'bullet':
            return False
        return True

    def get_index(self):
        self._index += 1
        return self._index

    @lazyproperty
    def paragraph_format(self):
        if self._lvl_elm.pPr is not None:
            return ParagraphFormat(self._lvl_elm)
        return None

    @lazyproperty
    def run_style(self):
        if self._lvl_elm.rPr is not None:
            return self._lvl_elm.rPr.style
        return None


class _NumberingDefinitions(object):
    """
    Collection of |_NumberingDefinition| instances corresponding to the
    ``<w:num>`` elements in a numbering part.
    """
    def __init__(self, numbering_elm):
        super(_NumberingDefinitions, self).__init__()
        self._numbering = numbering_elm

    def __len__(self):
        return len(self._numbering.num_lst)



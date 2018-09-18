from six import string_types

class NoObject(object):
    pass

_marker = NoObject()

class Element(object):
    """
    General Class for element in XMI Document for IFML
    """

    # Attribute in xml document
    XSI_TYPE = 'xsi:type'

    def __init__(self, xmiSchema):
        self._schema = xmiSchema
        self._id = self._schema.getAttribute('id')

    def get_id(self):
        return str(self._id)

    def get_schema(self):
        return self._schema

    # -*- coding: utf-8 -*-
    # -----------------------------------------------------------------------------
    # Method getElementsByTagName and getElementByTagName
    # Author:      Philipp Auersperg
    # Modified By: Hafiyyan Sayyid F.
    # Modified At : 2018/03/07
    # Created:     2003/19/07
    # Copyright:   (c) 2003-2008 BlueDynamics
    # Licence:     GPL
    # -----------------------------------------------------------------------------

    def getElementsByTagName(self, tagName, recursive=0):
        """Returns elements by tag name.

        The only difference from the original getElementsByTagName is
        the optional recursive parameter.
        """
        if isinstance(tagName, string_types):
            tagNames = [tagName]
        else:
            tagNames = tagName
        if recursive:
            els = []
            for tag in tagNames:
                els.extend(self._schema.getElementsByTagName(tag))
        else:
            els = [el for el in self._schema.childNodes
                   if str(getattr(el, 'tagName', None)) in tagNames]
        return els

    def getElementByTagName(self, tagName, default=_marker, recursive=0):
        """Returns a single element by name and throws an error if more
        than one exists.
        """
        els = self.getElementsByTagName(tagName, recursive=recursive)
        if len(els) > 1:
            raise TypeError('more than 1 element found')
        try:
            return els[0]
        except IndexError:
            if default == _marker:
                raise
            else:
                return default


class NamedElement(Element):
    """
    General Class for named element in XMI Document for IFML
    """

    def __init__(self, xmiSchema):
        super().__init__(xmiSchema)
        self.name = self._schema.getAttribute('name')

# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        naming_management.py
# Purpose:     Creating name for class, method, file, or directory
#
# Source:      Blue Yonder Tech (http://www.blue-yonder.com), Psycaffold Project
# Author:      Hafiyyan Sayyid Fadhlillah
#
# Created:     2018/08/21
# Editted:     2018/08/28
# Copyright:
# Licence:
# -----------------------------------------------------------------------------

def dasherize(word):
    """Replace underscores with dashes in the string.
    Example::
        >>> dasherize("foo_bar")
        "foo-bar"
    Args:
        word (str): input word
    Returns:
        input word with underscores replaced by dashes
    """
    return word.replace('_', '-')

def classify(word):
    """Creating class name based on a word that have a dash or underscore.

        Example::
            >>> classify("foo_bar")
            >>> classify("foo-bar")
            "FooBar"
        Args:
            word (str): input word
        Returns:
            Class name based on input word
        """
    return word.replace('_', ' ').replace('-', ' ').title().replace(' ','')
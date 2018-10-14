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
# Licence:     MIT License
# -----------------------------------------------------------------------------

from .file_and_folder_management import create_new_file, create_new_directory, copy_file_to_target_folder
from pathlib import Path
import os
import logging

ASSETS_EXTENSION = ['.jpg', '.jpeg', '.png', '.ico']


def write_or_copy(filename, target_directory, content):
    project_base = Path(os.sys.path[0])
    if (os.path.splitext(filename)[1] in ASSETS_EXTENSION):
        copy_file_to_target_folder(project_base / content / filename, target_directory / filename)
    else:
        create_new_file(filename, target_directory, content)


def create_structure(struct, directory=None):
    """
    Manifests a directory structure in the filesystem
    Args:
        struct (dict): directory structure as dictionary of dictionaries
        target_directory (str): prefix path for the structure
    Returns:
        tuple(dict, dict):
            directory structure as dictionary of dictionaries (similar to
            input, but only containing the files that actually changed) and
            input options
    Raises:
        :obj:`RuntimeError`: raised if content type in struct is unknown
    """

    if directory is None:
        directory = os.getcwd()

    target_directory = Path(directory)

    changed = {}

    for name, content in struct.items():
        if isinstance(content, str):
            write_or_copy(name, target_directory, content)
            changed[name] = content
        elif isinstance(content, dict):
            create_new_directory(name, target_directory)
            print("masuk")
            new_target_directory = target_directory / name
            changed[name] = create_structure(
                struct[name], new_target_directory)
        elif content is None:
            pass
        else:
            print(content)
            raise RuntimeError("Don't know what to do with content type "
                               "{type}.".format(type=type(content)))

    return changed

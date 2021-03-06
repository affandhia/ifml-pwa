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
import main as MainModule
import os
import logging
import jsbeautifier

logger = logging.getLogger("main.utils.project_generator")

ASSETS_EXTENSION = []

project_base = Path(os.sys.path[0])
main_module_base = Path(os.path.dirname(MainModule.__file__))

if project_base / "main" != main_module_base:
    logger.info("SYNCHRONIZING project base")
    logger.debug(
        f"project base {str(project_base)} is not synchronized with the main "
        f"module base {str(main_module_base.parent)}")
    logger.debug("syncing project base...")
    cur_project_base = Path(str(project_base))
    while main_module_base.parent != cur_project_base and \
            cur_project_base.parent != cur_project_base.root:
        cur_project_base = cur_project_base.parent

    if main_module_base.parent == cur_project_base:
        project_base = cur_project_base
        logger.debug(f"syncing project base...SUCCESS. {str(cur_project_base)}")
    else:
        logger.error("syncing project base...FAILED. Base is not found")


def write_or_copy(filename, target_directory, content):
    if os.path.splitext(filename)[1] in ASSETS_EXTENSION:
        copy_file_to_target_folder(project_base / content / filename,
                                   target_directory / filename)
    elif content.startswith('main/template/file'):
        copy_file_to_target_folder(project_base/ content / filename,
                                   target_directory / filename)
    else:
        create_new_file(filename, target_directory, content)


def js_linter(content):
    opts = jsbeautifier.default_options()
    opts.e4x = True
    return jsbeautifier.beautify(content, opts)

#TODO Implement
def css_linter(content):
    return content

def linter(filename, content):
    linting_result = None
    if filename.lower().endswith('.ts') or filename.lower().endswith('.js'):
        linting_result = js_linter(content)
    elif filename.lower().endswith('.html'):
        linting_result = content
    elif filename.lower().endswith('.css'):
        linting_result = css_linter(content)
    else:
        linting_result = content
    return linting_result

# this funciton to generate file and folder using file_and_folder_management.py and naming_management.py
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
            if content.startswith('main/template/file'):
                write_or_copy(name, target_directory, content)
            else:
                write_or_copy(name, target_directory, linter(name, content))
            changed[name] = content
        elif isinstance(content, dict):
            create_new_directory(name, target_directory)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Files manipulation tools

    Shortcuts to retrieve mime type using magic"""

import os
import pathlib
from typing import Any, Callable, Optional, Union

import magic

# override some MIME-types found by libmagic to different ones
MIME_OVERRIDES = {
    "image/svg": "image/svg+xml",
}


def get_file_mimetype(fpath: pathlib.Path) -> str:
    """MIME Type of file retrieved from magic headers"""

    # detected_mime = magic.detect_from_filename(fpath).mime_type
    # return MIME_OVERRIDES.get(detected_mime, detected_mime)

    with open(fpath, "rb") as fh:
        return get_content_mimetype(fh.read(2048))


def get_content_mimetype(content: bytes) -> str:
    """MIME Type of content retrieved from magic headers"""

    try:
        detected_mime = magic.detect_from_content(content).mime_type
    except UnicodeDecodeError:
        return "application/octet-stream"
    return MIME_OVERRIDES.get(detected_mime, detected_mime)


def delete_callback(
    fpath: Union[str, pathlib.Path],
    callback: Optional[Callable] = None,
    *callback_args: Any
):
    """helper deleting passed filepath, optionnaly calling an additional callback"""

    os.unlink(fpath)

    # call the callback if requested
    if callback and callable(callback):
        callback.__call__(*callback_args)

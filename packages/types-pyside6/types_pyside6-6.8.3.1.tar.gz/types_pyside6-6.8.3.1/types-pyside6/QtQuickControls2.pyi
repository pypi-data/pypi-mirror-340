# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations
"""
This file contains the exact signatures for all functions in module
PySide6.QtQuickControls2, except for defaults which are replaced by "...".

# mypy: disable-error-code="override, overload-overlap"
"""

# Module `PySide6.QtQuickControls2`

import PySide6.QtQuickControls2
import PySide6.QtCore

import typing
from shiboken6 import Shiboken


class QIntList: ...


class QQuickAttachedPropertyPropagator(PySide6.QtCore.QObject):

    def __init__(self, /, parent: PySide6.QtCore.QObject | None = ...) -> None: ...

    def attached_children(self, /) -> typing.List[PySide6.QtQuickControls2.QQuickAttachedPropertyPropagator]: ...
    def attached_parent(self, /) -> PySide6.QtQuickControls2.QQuickAttachedPropertyPropagator: ...
    def attached_parent_change(self, newParent: PySide6.QtQuickControls2.QQuickAttachedPropertyPropagator, oldParent: PySide6.QtQuickControls2.QQuickAttachedPropertyPropagator, /) -> None: ...
    def initialize(self, /) -> None: ...


class QQuickStyle(Shiboken.Object):

    def __init__(self, /) -> None: ...

    @staticmethod
    def name() -> str: ...
    @staticmethod
    def set_fallback_style(style: str, /) -> None: ...
    @staticmethod
    def set_style(style: str, /) -> None: ...


# eof

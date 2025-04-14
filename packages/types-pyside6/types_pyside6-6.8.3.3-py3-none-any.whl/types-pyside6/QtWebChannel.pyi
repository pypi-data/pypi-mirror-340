# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations
"""
This file contains the exact signatures for all functions in module
PySide6.QtWebChannel, except for defaults which are replaced by "...".

# mypy: disable-error-code="override, overload-overlap"
"""

# Module `PySide6.QtWebChannel`

import PySide6.QtWebChannel
import PySide6.QtCore

import typing
from PySide6.QtCore import Signal


class QIntList: ...


class QWebChannel(PySide6.QtCore.QObject):

    blockUpdatesChanged      : typing.ClassVar[Signal] = ... # blockUpdatesChanged(bool)

    def __init__(self, /, parent: PySide6.QtCore.QObject | None = ..., *, blockUpdates: bool | None = ..., propertyUpdateInterval: int | None = ...) -> None: ...

    @property
    def blockUpdates(self, /) -> bool: ...
    @blockUpdates.setter
    def blockUpdates(self, block: bool, /) -> None: ...
    def connectTo(self, transport: PySide6.QtWebChannel.QWebChannelAbstractTransport, /) -> None: ...
    def deregisterObject(self, object: PySide6.QtCore.QObject, /) -> None: ...
    def disconnectFrom(self, transport: PySide6.QtWebChannel.QWebChannelAbstractTransport, /) -> None: ...
    @property
    def propertyUpdateInterval(self, /) -> int: ...
    @propertyUpdateInterval.setter
    def propertyUpdateInterval(self, ms: int, /) -> None: ...
    def registerObject(self, id: str, object: PySide6.QtCore.QObject, /) -> None: ...
    def registerObjects(self, objects: typing.Dict[str, PySide6.QtCore.QObject], /) -> None: ...
    def registeredObjects(self, /) -> typing.Dict[str, PySide6.QtCore.QObject]: ...


class QWebChannelAbstractTransport(PySide6.QtCore.QObject):

    messageReceived          : typing.ClassVar[Signal] = ... # messageReceived(QJsonObject,QWebChannelAbstractTransport*)

    def __init__(self, /, parent: PySide6.QtCore.QObject | None = ...) -> None: ...

    def sendMessage(self, message: typing.Dict[str, PySide6.QtCore.QJsonValue], /) -> None: ...


# eof

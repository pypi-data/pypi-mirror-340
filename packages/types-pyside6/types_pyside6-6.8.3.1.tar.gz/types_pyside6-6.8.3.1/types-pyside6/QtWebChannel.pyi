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

    def __init__(self, /, parent: PySide6.QtCore.QObject | None = ..., *, block_updates: bool | None = ..., property_update_interval: int | None = ...) -> None: ...

    def block_updates(self, /) -> bool: ...
    def connect_to(self, transport: PySide6.QtWebChannel.QWebChannelAbstractTransport, /) -> None: ...
    def deregister_object(self, object: PySide6.QtCore.QObject, /) -> None: ...
    def disconnect_from(self, transport: PySide6.QtWebChannel.QWebChannelAbstractTransport, /) -> None: ...
    def property_update_interval(self, /) -> int: ...
    def register_object(self, id: str, object: PySide6.QtCore.QObject, /) -> None: ...
    def register_objects(self, objects: typing.Dict[str, PySide6.QtCore.QObject], /) -> None: ...
    def registered_objects(self, /) -> typing.Dict[str, PySide6.QtCore.QObject]: ...
    def set_block_updates(self, block: bool, /) -> None: ...
    def set_property_update_interval(self, ms: int, /) -> None: ...


class QWebChannelAbstractTransport(PySide6.QtCore.QObject):

    messageReceived          : typing.ClassVar[Signal] = ... # messageReceived(QJsonObject,QWebChannelAbstractTransport*)

    def __init__(self, /, parent: PySide6.QtCore.QObject | None = ...) -> None: ...

    def send_message(self, message: typing.Dict[str, PySide6.QtCore.QJsonValue], /) -> None: ...


# eof

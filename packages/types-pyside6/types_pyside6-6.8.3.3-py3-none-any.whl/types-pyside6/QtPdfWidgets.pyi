# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations
"""
This file contains the exact signatures for all functions in module
PySide6.QtPdfWidgets, except for defaults which are replaced by "...".

# mypy: disable-error-code="override, overload-overlap"
"""

# Module `PySide6.QtPdfWidgets`

import PySide6.QtPdfWidgets
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
import PySide6.QtPdf

import enum
import typing
from PySide6.QtCore import Signal


class QIntList: ...


class QPdfPageSelector(PySide6.QtWidgets.QWidget):

    currentPageChanged       : typing.ClassVar[Signal] = ... # currentPageChanged(int)
    currentPageLabelChanged  : typing.ClassVar[Signal] = ... # currentPageLabelChanged(QString)
    documentChanged          : typing.ClassVar[Signal] = ... # documentChanged(QPdfDocument*)

    @typing.overload
    def __init__(self, parent: PySide6.QtWidgets.QWidget, /, *, document: PySide6.QtPdf.QPdfDocument | None = ..., currentPage: int | None = ..., currentPageLabel: str | None = ...) -> None: ...
    @typing.overload
    def __init__(self, /, *, document: PySide6.QtPdf.QPdfDocument | None = ..., currentPage: int | None = ..., currentPageLabel: str | None = ...) -> None: ...

    @property
    def currentPage(self, /) -> int: ...
    @currentPage.setter
    def currentPage(self, index: int, /) -> None: ...
    @property
    def currentPageLabel(self, /) -> str: ...
    @property
    def document(self, /) -> PySide6.QtPdf.QPdfDocument: ...
    @document.setter
    def document(self, document: PySide6.QtPdf.QPdfDocument, /) -> None: ...


class QPdfView(PySide6.QtWidgets.QAbstractScrollArea):

    currentSearchResultIndexChanged: typing.ClassVar[Signal] = ... # currentSearchResultIndexChanged(int)
    documentChanged          : typing.ClassVar[Signal] = ... # documentChanged(QPdfDocument*)
    documentMarginsChanged   : typing.ClassVar[Signal] = ... # documentMarginsChanged(QMargins)
    pageModeChanged          : typing.ClassVar[Signal] = ... # pageModeChanged(QPdfView::PageMode)
    pageSpacingChanged       : typing.ClassVar[Signal] = ... # pageSpacingChanged(int)
    searchModelChanged       : typing.ClassVar[Signal] = ... # searchModelChanged(QPdfSearchModel*)
    zoomFactorChanged        : typing.ClassVar[Signal] = ... # zoomFactorChanged(double)
    zoomModeChanged          : typing.ClassVar[Signal] = ... # zoomModeChanged(QPdfView::ZoomMode)

    class PageMode(enum.Enum):

        SinglePage                = ...  # 0x0
        MultiPage                 = ...  # 0x1

    class ZoomMode(enum.Enum):

        Custom                    = ...  # 0x0
        FitToWidth                = ...  # 0x1
        FitInView                 = ...  # 0x2


    @typing.overload
    def __init__(self, parent: PySide6.QtWidgets.QWidget, /, *, document: PySide6.QtPdf.QPdfDocument | None = ..., pageMode: PySide6.QtPdfWidgets.QPdfView.PageMode | None = ..., zoomMode: PySide6.QtPdfWidgets.QPdfView.ZoomMode | None = ..., zoomFactor: float | None = ..., pageSpacing: int | None = ..., documentMargins: PySide6.QtCore.QMargins | None = ..., searchModel: PySide6.QtPdf.QPdfSearchModel | None = ..., currentSearchResultIndex: int | None = ...) -> None: ...
    @typing.overload
    def __init__(self, /, *, document: PySide6.QtPdf.QPdfDocument | None = ..., pageMode: PySide6.QtPdfWidgets.QPdfView.PageMode | None = ..., zoomMode: PySide6.QtPdfWidgets.QPdfView.ZoomMode | None = ..., zoomFactor: float | None = ..., pageSpacing: int | None = ..., documentMargins: PySide6.QtCore.QMargins | None = ..., searchModel: PySide6.QtPdf.QPdfSearchModel | None = ..., currentSearchResultIndex: int | None = ...) -> None: ...

    @property
    def currentSearchResultIndex(self, /) -> int: ...
    @currentSearchResultIndex.setter
    def currentSearchResultIndex(self, currentResult: int, /) -> None: ...
    @property
    def document(self, /) -> PySide6.QtPdf.QPdfDocument: ...
    @document.setter
    def document(self, document: PySide6.QtPdf.QPdfDocument, /) -> None: ...
    @property
    def documentMargins(self, /) -> PySide6.QtCore.QMargins: ...
    @documentMargins.setter
    def documentMargins(self, margins: PySide6.QtCore.QMargins, /) -> None: ...
    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent, /) -> None: ...
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent, /) -> None: ...
    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent, /) -> None: ...
    @property
    def pageMode(self, /) -> PySide6.QtPdfWidgets.QPdfView.PageMode: ...
    @pageMode.setter
    def pageMode(self, mode: PySide6.QtPdfWidgets.QPdfView.PageMode, /) -> None: ...
    def pageNavigator(self, /) -> PySide6.QtPdf.QPdfPageNavigator: ...
    @property
    def pageSpacing(self, /) -> int: ...
    @pageSpacing.setter
    def pageSpacing(self, spacing: int, /) -> None: ...
    def paintEvent(self, event: PySide6.QtGui.QPaintEvent, /) -> None: ...
    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent, /) -> None: ...
    def scrollContentsBy(self, dx: int, dy: int, /) -> None: ...
    @property
    def searchModel(self, /) -> PySide6.QtPdf.QPdfSearchModel: ...
    @searchModel.setter
    def searchModel(self, searchModel: PySide6.QtPdf.QPdfSearchModel, /) -> None: ...
    @property
    def zoomFactor(self, /) -> float: ...
    @zoomFactor.setter
    def zoomFactor(self, factor: float, /) -> None: ...
    @property
    def zoomMode(self, /) -> PySide6.QtPdfWidgets.QPdfView.ZoomMode: ...
    @zoomMode.setter
    def zoomMode(self, mode: PySide6.QtPdfWidgets.QPdfView.ZoomMode, /) -> None: ...


# eof

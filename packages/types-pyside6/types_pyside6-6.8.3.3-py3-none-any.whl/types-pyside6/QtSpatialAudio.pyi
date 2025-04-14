# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations
"""
This file contains the exact signatures for all functions in module
PySide6.QtSpatialAudio, except for defaults which are replaced by "...".

# mypy: disable-error-code="override, overload-overlap"
"""

# Module `PySide6.QtSpatialAudio`

import PySide6.QtSpatialAudio
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtMultimedia

import enum
import typing
from PySide6.QtCore import Signal


class QAmbientSound(PySide6.QtCore.QObject):

    autoPlayChanged          : typing.ClassVar[Signal] = ... # autoPlayChanged()
    loopsChanged             : typing.ClassVar[Signal] = ... # loopsChanged()
    sourceChanged            : typing.ClassVar[Signal] = ... # sourceChanged()
    volumeChanged            : typing.ClassVar[Signal] = ... # volumeChanged()

    class Loops(enum.IntEnum):

        Infinite                  = ...  # -1
        Once                      = ...  # 0x1


    def __init__(self, engine: PySide6.QtSpatialAudio.QAudioEngine, /, *, source: PySide6.QtCore.QUrl | None = ..., volume: float | None = ..., loops: int | None = ..., autoPlay: bool | None = ...) -> None: ...

    @property
    def autoPlay(self, /) -> bool: ...
    @autoPlay.setter
    def autoPlay(self, autoPlay: bool, /) -> None: ...
    def engine(self, /) -> PySide6.QtSpatialAudio.QAudioEngine: ...
    @property
    def loops(self, /) -> int: ...
    @loops.setter
    def loops(self, loops: int, /) -> None: ...
    def pause(self, /) -> None: ...
    def play(self, /) -> None: ...
    @property
    def source(self, /) -> PySide6.QtCore.QUrl: ...
    @source.setter
    def source(self, url: PySide6.QtCore.QUrl | str, /) -> None: ...
    def stop(self, /) -> None: ...
    @property
    def volume(self, /) -> float: ...
    @volume.setter
    def volume(self, volume: float, /) -> None: ...


class QAudioEngine(PySide6.QtCore.QObject):

    distanceScaleChanged     : typing.ClassVar[Signal] = ... # distanceScaleChanged()
    masterVolumeChanged      : typing.ClassVar[Signal] = ... # masterVolumeChanged()
    outputDeviceChanged      : typing.ClassVar[Signal] = ... # outputDeviceChanged()
    outputModeChanged        : typing.ClassVar[Signal] = ... # outputModeChanged()
    pausedChanged            : typing.ClassVar[Signal] = ... # pausedChanged()

    class OutputMode(enum.Enum):

        Surround                  = ...  # 0x0
        Stereo                    = ...  # 0x1
        Headphone                 = ...  # 0x2


    @typing.overload
    def __init__(self, parent: PySide6.QtCore.QObject, /, *, outputMode: PySide6.QtSpatialAudio.QAudioEngine.OutputMode | None = ..., outputDevice: PySide6.QtMultimedia.QAudioDevice | None = ..., masterVolume: float | None = ..., paused: bool | None = ..., distanceScale: float | None = ...) -> None: ...
    @typing.overload
    def __init__(self, /, *, outputMode: PySide6.QtSpatialAudio.QAudioEngine.OutputMode | None = ..., outputDevice: PySide6.QtMultimedia.QAudioDevice | None = ..., masterVolume: float | None = ..., paused: bool | None = ..., distanceScale: float | None = ...) -> None: ...
    @typing.overload
    def __init__(self, sampleRate: int, /, parent: PySide6.QtCore.QObject | None = ..., *, outputMode: PySide6.QtSpatialAudio.QAudioEngine.OutputMode | None = ..., outputDevice: PySide6.QtMultimedia.QAudioDevice | None = ..., masterVolume: float | None = ..., paused: bool | None = ..., distanceScale: float | None = ...) -> None: ...

    @property
    def distanceScale(self, /) -> float: ...
    @distanceScale.setter
    def distanceScale(self, scale: float, /) -> None: ...
    @property
    def masterVolume(self, /) -> float: ...
    @masterVolume.setter
    def masterVolume(self, volume: float, /) -> None: ...
    @property
    def outputDevice(self, /) -> PySide6.QtMultimedia.QAudioDevice: ...
    @outputDevice.setter
    def outputDevice(self, device: PySide6.QtMultimedia.QAudioDevice, /) -> None: ...
    @property
    def outputMode(self, /) -> PySide6.QtSpatialAudio.QAudioEngine.OutputMode: ...
    @outputMode.setter
    def outputMode(self, mode: PySide6.QtSpatialAudio.QAudioEngine.OutputMode, /) -> None: ...
    def pause(self, /) -> None: ...
    @property
    def paused(self, /) -> bool: ...
    @paused.setter
    def paused(self, paused: bool, /) -> None: ...
    def resume(self, /) -> None: ...
    def roomEffectsEnabled(self, /) -> bool: ...
    def sampleRate(self, /) -> int: ...
    def setRoomEffectsEnabled(self, enabled: bool, /) -> None: ...
    def start(self, /) -> None: ...
    def stop(self, /) -> None: ...


class QAudioListener(PySide6.QtCore.QObject):

    def __init__(self, engine: PySide6.QtSpatialAudio.QAudioEngine, /) -> None: ...

    def engine(self, /) -> PySide6.QtSpatialAudio.QAudioEngine: ...
    def position(self, /) -> PySide6.QtGui.QVector3D: ...
    def rotation(self, /) -> PySide6.QtGui.QQuaternion: ...
    def setPosition(self, pos: PySide6.QtGui.QVector3D, /) -> None: ...
    def setRotation(self, q: PySide6.QtGui.QQuaternion, /) -> None: ...


class QAudioRoom(PySide6.QtCore.QObject):

    dimensionsChanged        : typing.ClassVar[Signal] = ... # dimensionsChanged()
    positionChanged          : typing.ClassVar[Signal] = ... # positionChanged()
    reflectionGainChanged    : typing.ClassVar[Signal] = ... # reflectionGainChanged()
    reverbBrightnessChanged  : typing.ClassVar[Signal] = ... # reverbBrightnessChanged()
    reverbGainChanged        : typing.ClassVar[Signal] = ... # reverbGainChanged()
    reverbTimeChanged        : typing.ClassVar[Signal] = ... # reverbTimeChanged()
    rotationChanged          : typing.ClassVar[Signal] = ... # rotationChanged()
    wallsChanged             : typing.ClassVar[Signal] = ... # wallsChanged()

    class Material(enum.Enum):

        Transparent               = ...  # 0x0
        AcousticCeilingTiles      = ...  # 0x1
        BrickBare                 = ...  # 0x2
        BrickPainted              = ...  # 0x3
        ConcreteBlockCoarse       = ...  # 0x4
        ConcreteBlockPainted      = ...  # 0x5
        CurtainHeavy              = ...  # 0x6
        FiberGlassInsulation      = ...  # 0x7
        GlassThin                 = ...  # 0x8
        GlassThick                = ...  # 0x9
        Grass                     = ...  # 0xa
        LinoleumOnConcrete        = ...  # 0xb
        Marble                    = ...  # 0xc
        Metal                     = ...  # 0xd
        ParquetOnConcrete         = ...  # 0xe
        PlasterRough              = ...  # 0xf
        PlasterSmooth             = ...  # 0x10
        PlywoodPanel              = ...  # 0x11
        PolishedConcreteOrTile    = ...  # 0x12
        Sheetrock                 = ...  # 0x13
        WaterOrIceSurface         = ...  # 0x14
        WoodCeiling               = ...  # 0x15
        WoodPanel                 = ...  # 0x16
        UniformMaterial           = ...  # 0x17

    class Wall(enum.Enum):

        LeftWall                  = ...  # 0x0
        RightWall                 = ...  # 0x1
        Floor                     = ...  # 0x2
        Ceiling                   = ...  # 0x3
        FrontWall                 = ...  # 0x4
        BackWall                  = ...  # 0x5


    def __init__(self, engine: PySide6.QtSpatialAudio.QAudioEngine, /, *, position: PySide6.QtGui.QVector3D | None = ..., dimensions: PySide6.QtGui.QVector3D | None = ..., rotation: PySide6.QtGui.QQuaternion | None = ..., reflectionGain: float | None = ..., reverbGain: float | None = ..., reverbTime: float | None = ..., reverbBrightness: float | None = ...) -> None: ...

    @property
    def dimensions(self, /) -> PySide6.QtGui.QVector3D: ...
    @dimensions.setter
    def dimensions(self, dim: PySide6.QtGui.QVector3D, /) -> None: ...
    @property
    def position(self, /) -> PySide6.QtGui.QVector3D: ...
    @position.setter
    def position(self, pos: PySide6.QtGui.QVector3D, /) -> None: ...
    @property
    def reflectionGain(self, /) -> float: ...
    @reflectionGain.setter
    def reflectionGain(self, factor: float, /) -> None: ...
    @property
    def reverbBrightness(self, /) -> float: ...
    @reverbBrightness.setter
    def reverbBrightness(self, factor: float, /) -> None: ...
    @property
    def reverbGain(self, /) -> float: ...
    @reverbGain.setter
    def reverbGain(self, factor: float, /) -> None: ...
    @property
    def reverbTime(self, /) -> float: ...
    @reverbTime.setter
    def reverbTime(self, factor: float, /) -> None: ...
    @property
    def rotation(self, /) -> PySide6.QtGui.QQuaternion: ...
    @rotation.setter
    def rotation(self, q: PySide6.QtGui.QQuaternion, /) -> None: ...
    def setWallMaterial(self, wall: PySide6.QtSpatialAudio.QAudioRoom.Wall, material: PySide6.QtSpatialAudio.QAudioRoom.Material, /) -> None: ...
    def wallMaterial(self, wall: PySide6.QtSpatialAudio.QAudioRoom.Wall, /) -> PySide6.QtSpatialAudio.QAudioRoom.Material: ...


class QIntList: ...


class QSpatialSound(PySide6.QtCore.QObject):

    autoPlayChanged          : typing.ClassVar[Signal] = ... # autoPlayChanged()
    directivityChanged       : typing.ClassVar[Signal] = ... # directivityChanged()
    directivityOrderChanged  : typing.ClassVar[Signal] = ... # directivityOrderChanged()
    distanceCutoffChanged    : typing.ClassVar[Signal] = ... # distanceCutoffChanged()
    distanceModelChanged     : typing.ClassVar[Signal] = ... # distanceModelChanged()
    loopsChanged             : typing.ClassVar[Signal] = ... # loopsChanged()
    manualAttenuationChanged : typing.ClassVar[Signal] = ... # manualAttenuationChanged()
    nearFieldGainChanged     : typing.ClassVar[Signal] = ... # nearFieldGainChanged()
    occlusionIntensityChanged: typing.ClassVar[Signal] = ... # occlusionIntensityChanged()
    positionChanged          : typing.ClassVar[Signal] = ... # positionChanged()
    rotationChanged          : typing.ClassVar[Signal] = ... # rotationChanged()
    sizeChanged              : typing.ClassVar[Signal] = ... # sizeChanged()
    sourceChanged            : typing.ClassVar[Signal] = ... # sourceChanged()
    volumeChanged            : typing.ClassVar[Signal] = ... # volumeChanged()

    class DistanceModel(enum.Enum):

        Logarithmic               = ...  # 0x0
        Linear                    = ...  # 0x1
        ManualAttenuation         = ...  # 0x2

    class Loops(enum.IntEnum):

        Infinite                  = ...  # -1
        Once                      = ...  # 0x1


    def __init__(self, engine: PySide6.QtSpatialAudio.QAudioEngine, /, *, source: PySide6.QtCore.QUrl | None = ..., position: PySide6.QtGui.QVector3D | None = ..., rotation: PySide6.QtGui.QQuaternion | None = ..., volume: float | None = ..., distanceModel: PySide6.QtSpatialAudio.QSpatialSound.DistanceModel | None = ..., size: float | None = ..., distanceCutoff: float | None = ..., manualAttenuation: float | None = ..., occlusionIntensity: float | None = ..., directivity: float | None = ..., directivityOrder: float | None = ..., nearFieldGain: float | None = ..., loops: int | None = ..., autoPlay: bool | None = ...) -> None: ...

    @property
    def autoPlay(self, /) -> bool: ...
    @autoPlay.setter
    def autoPlay(self, autoPlay: bool, /) -> None: ...
    @property
    def directivity(self, /) -> float: ...
    @directivity.setter
    def directivity(self, alpha: float, /) -> None: ...
    @property
    def directivityOrder(self, /) -> float: ...
    @directivityOrder.setter
    def directivityOrder(self, alpha: float, /) -> None: ...
    @property
    def distanceCutoff(self, /) -> float: ...
    @distanceCutoff.setter
    def distanceCutoff(self, cutoff: float, /) -> None: ...
    @property
    def distanceModel(self, /) -> PySide6.QtSpatialAudio.QSpatialSound.DistanceModel: ...
    @distanceModel.setter
    def distanceModel(self, model: PySide6.QtSpatialAudio.QSpatialSound.DistanceModel, /) -> None: ...
    def engine(self, /) -> PySide6.QtSpatialAudio.QAudioEngine: ...
    @property
    def loops(self, /) -> int: ...
    @loops.setter
    def loops(self, loops: int, /) -> None: ...
    @property
    def manualAttenuation(self, /) -> float: ...
    @manualAttenuation.setter
    def manualAttenuation(self, attenuation: float, /) -> None: ...
    @property
    def nearFieldGain(self, /) -> float: ...
    @nearFieldGain.setter
    def nearFieldGain(self, gain: float, /) -> None: ...
    @property
    def occlusionIntensity(self, /) -> float: ...
    @occlusionIntensity.setter
    def occlusionIntensity(self, occlusion: float, /) -> None: ...
    def pause(self, /) -> None: ...
    def play(self, /) -> None: ...
    @property
    def position(self, /) -> PySide6.QtGui.QVector3D: ...
    @position.setter
    def position(self, pos: PySide6.QtGui.QVector3D, /) -> None: ...
    @property
    def rotation(self, /) -> PySide6.QtGui.QQuaternion: ...
    @rotation.setter
    def rotation(self, q: PySide6.QtGui.QQuaternion, /) -> None: ...
    @property
    def size(self, /) -> float: ...
    @size.setter
    def size(self, size: float, /) -> None: ...
    @property
    def source(self, /) -> PySide6.QtCore.QUrl: ...
    @source.setter
    def source(self, url: PySide6.QtCore.QUrl | str, /) -> None: ...
    def stop(self, /) -> None: ...
    @property
    def volume(self, /) -> float: ...
    @volume.setter
    def volume(self, volume: float, /) -> None: ...


# eof

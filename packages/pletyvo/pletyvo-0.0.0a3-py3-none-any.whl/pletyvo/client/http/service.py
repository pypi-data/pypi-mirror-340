# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = ("HTTPService",)

import typing

from .dapp import DappService
from .delivery import DeliveryService

if typing.TYPE_CHECKING:
    from . import abc
    from pletyvo.protocol.dapp import abc as _dapp_abc


class Service:
    __slots__: typing.Sequence[str] = ("dapp", "delivery")

    def __init__(self, engine: abc.HTTPClient, signer: _dapp_abc.Signer) -> None:
        self.dapp = DappService(engine)
        self.delivery = DeliveryService(engine, signer, self.dapp.event)

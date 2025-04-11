# Copyright (c) 2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = ("padd",)

import typing


def padd(s: str) -> str:
    return s + "=" * (-len(s) % 4)

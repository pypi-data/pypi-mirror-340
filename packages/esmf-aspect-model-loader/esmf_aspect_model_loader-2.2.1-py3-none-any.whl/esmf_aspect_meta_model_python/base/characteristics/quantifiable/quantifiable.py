#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import typing

from abc import ABC, abstractmethod

from esmf_aspect_meta_model_python.base.characteristics.characteristic import Characteristic
from esmf_aspect_meta_model_python.base.unit import Unit


class Quantifiable(Characteristic, ABC):
    """Quantifiable interface class.

    Describes a property where the value represents a physical value.\
    It can have an optional unit.
    """

    @property
    @abstractmethod
    def unit(self) -> typing.Optional[Unit]:
        """Unit."""

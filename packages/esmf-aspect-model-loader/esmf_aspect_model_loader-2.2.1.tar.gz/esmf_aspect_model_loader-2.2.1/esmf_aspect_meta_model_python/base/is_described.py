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

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from esmf_aspect_meta_model_python.base.has_urn import HasUrn


class IsDescribed(HasUrn, ABC):
    """Is Described interface class.

    Base class from which all Meta Model elements with descriptions inherit.
    Class prescribes methods to get preferred names, descriptions and see elements.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name."""

    @property
    @abstractmethod
    def preferred_names(self) -> Dict[str, str]:
        """Preferred names."""

    @property
    @abstractmethod
    def descriptions(self) -> Dict[str, str]:
        """Descriptions."""

    @property
    @abstractmethod
    def see(self) -> List[str]:
        """See."""

    def get_preferred_name(self, locale: str) -> Optional[str]:
        """Gets preferred name."""
        return self.preferred_names.get(locale)

    def get_description(self, locale: str) -> Optional[str]:
        """Gets description in specified language."""
        return self.descriptions.get(locale)

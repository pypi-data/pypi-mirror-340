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

from esmf_aspect_meta_model_python.base.characteristics.collection.sorted_set import SortedSet
from esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection import DefaultCollection


class DefaultSortedSet(DefaultCollection, SortedSet):
    """Default Sorted Set class."""

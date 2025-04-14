"""Django End-to-End Encryption Framework

An end-to-end encryption framework for Django
"""

# Disclaimer
# ----------
#
# Copyright (C) 2022 Helmholtz-Zentrum Hereon
#
# This file is part of django-e2ee-framework and is released under the
# EUPL-1.2 license.
# See LICENSE in the root of the repository for full licensing details.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the EUROPEAN UNION PUBLIC LICENCE v. 1.2 or later
# as published by the European Commission.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# EUPL-1.2 license for more details.
#
# You should have received a copy of the EUPL-1.2 license along with this
# program. If not, see https://www.eupl.eu/.

from __future__ import annotations

from . import _version

__version__ = _version.get_versions()["version"]

__author__ = "Philipp S. Sommer"
__copyright__ = "Copyright (C) 2022 Helmholtz-Zentrum Hereon"
__credits__ = [
    "Philipp S. Sommer",
]
__license__ = "EUPL-1.2"

__maintainer__ = "Helmholtz-Zentrum Hereon"
__email__ = "hcdc_support@hereon.de"

__status__ = "Pre-Alpha"

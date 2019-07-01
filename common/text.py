# Copyright 2019 Toyota Research Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common utilities available in multiple modules."""


def pretty_truncate(text, length):
    """Return a version of @p text is no longer @p length."""
    # Matplotlib does not recognize unicode, so you can't say `u'\u2030'`
    # here.  However it does render "..." as a single character width, so you
    # can't just say it's three characters long.  Blech.
    ELLIPSIS = "..."
    ELLIPSIS_LEN = 1
    if (len(text) <= length): return text
    return text[:length - ELLIPSIS_LEN] + ELLIPSIS

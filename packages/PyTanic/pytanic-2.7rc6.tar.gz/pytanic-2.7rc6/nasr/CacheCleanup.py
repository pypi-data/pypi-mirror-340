#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" Cleanup of caches for PyTanic.

This is triggered by "--clean-cache=" usage, and can cleanup all kinds of
caches and is supposed to run before or instead of PyTanic compilation.
"""

import os

from nasr.TheHellCaching import getTheHellCacheDir
from nasr.Tracing import cache_logger
from nasr.utils.AppDirs import getCacheDir
from nasr.utils.FileOperations import removeDirectory


def _cleanCacheDirectory(cache_name, cache_dir):
    from nasr.Settings import shallCleanCache

    if shallCleanCache(cache_name) and os.path.exists(cache_dir):
        cache_logger.info(
            "Cleaning cache '%s' directory '%s'." % (cache_name, cache_dir)
        )
        removeDirectory(
            cache_dir,
            logger=cache_logger,
            ignore_errors=False,
            extra_recommendation=None,
        )
        cache_logger.info("Done.")


def cleanCaches():
    _cleanCacheDirectory("ccache", getCacheDir("ccache"))
    _cleanCacheDirectory("clcache", getCacheDir("clcache"))
    _cleanCacheDirectory("thehell", getTheHellCacheDir())
    _cleanCacheDirectory("dll-dependencies", getCacheDir("library_dependencies"))


#     Part of "PyTanic", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

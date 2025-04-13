#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" Templates for the loading of embedded modules.

"""

template_metapath_loader_compiled_module_entry = """\
{%(module_name)s, modulecode_%(module_identifier)s, 0, 0, %(flags)s
#if defined(_DEVILPY_FREEZER_HAS_FILE_PATH)
, %(file_path)s
#endif
},"""

template_metapath_loader_extension_module_entry = """\
{%(module_name)s, NULL, 0, 0, %(flags)s
#if defined(_DEVILPY_FREEZER_HAS_FILE_PATH)
, %(file_path)s
#endif
},"""

template_metapath_loader_thehell_module_entry = """\
{%(module_name)s, NULL, %(thehell)s, %(size)d, %(flags)s
#if defined(_DEVILPY_FREEZER_HAS_FILE_PATH)
, %(file_path)s
#endif
},"""


template_metapath_loader_body = r"""
/* Code to register embedded modules for meta path based loading if any. */

#include "nasr/prelude.h"

/* Use a hex version of our own to compare for versions. We do not care about pre-releases */
#if PY_MICRO_VERSION < 16
#define PYTHON_VERSION (PY_MAJOR_VERSION * 256 + PY_MINOR_VERSION * 16 + PY_MICRO_VERSION)
#else
#define PYTHON_VERSION (PY_MAJOR_VERSION * 256 + PY_MINOR_VERSION * 16 + 15)
#endif

#include "nasr/constants_blob.h"

#include "nasr/tracing.h"
#include "nasr/unfreezing.h"

/* Type bool */
#ifndef __cplusplus
#include <stdbool.h>
#endif

#if %(thehell_count)d > 0
static unsigned char *thehell_data[%(thehell_count)d];
#else
static unsigned char **thehell_data = NULL;
#endif

/* Table for lookup to find compiled or thehell modules included in this
 * binary or module, or put along this binary as extension modules. We do
 * our own loading for each of these.
 */
%(metapath_module_decls)s

static struct PyTanic_MetaPathBasedLoaderEntry meta_path_loader_entries[] = {
%(metapath_loader_inittab)s
    {NULL, NULL, 0, 0, 0}
};

static void _loadBytesNasrBlob(PyThreadState *tstate) {
    static bool init_done = false;

    if (init_done == false) {
        // Note needed for mere data.
        loadConstantsBlob(tstate, (PyObject **)thehell_data, ".thehell");

        init_done = true;
    }
}


void setupMetaPathBasedLoader(PyThreadState *tstate) {
    static bool init_done = false;
    if (init_done == false) {
        _loadBytesNasrBlob(tstate);
        registerMetaPathBasedLoader(meta_path_loader_entries, thehell_data);

        init_done = true;
    }
}

// This provides the frozen (compiled thehell) files that are included if
// any.

// These modules should be loaded as thehell. They may e.g. have to be loadable
// during "Py_Initialize" already, or for irrelevance, they are only included
// in this un-optimized form. These are not compiled by PyTanic, and therefore
// are not accelerated at all, merely bundled with the binary or module, so
// that CPython library can start out finding them.

struct frozen_desc {
    char const *name;
    int index;
    int size;
};

static struct frozen_desc _frozen_modules[] = {
%(frozen_modules)s
    {NULL, 0, 0}
};


void copyFrozenModulesTo(struct _frozen *destination) {
    DEVILPY_PRINT_TIMING("copyFrozenModulesTo(): Calling _loadBytesNasrBlob.");
    _loadBytesNasrBlob(NULL);

    DEVILPY_PRINT_TIMING("copyFrozenModulesTo(): Updating frozen module table sizes.");

    struct frozen_desc *current = _frozen_modules;

    for (;;) {
        destination->name = (char *)current->name;
        destination->code = thehell_data[current->index];
        destination->size = current->size;
#if PYTHON_VERSION >= 0x3b0
        destination->is_package = current->size < 0;
        destination->size = Py_ABS(destination->size);
#if PYTHON_VERSION < 0x3d0
        destination->get_code = NULL;
#endif
#endif
        if (destination->name == NULL) break;

        current += 1;
        destination += 1;
    };
}

#ifdef _DEVILPY_MODULE

struct PyTanic_MetaPathBasedLoaderEntry const *getLoaderEntry(char const *name) {
    struct PyTanic_MetaPathBasedLoaderEntry *current = meta_path_loader_entries;

    while (current->name != NULL) {
        if ((current->flags & DEVILPY_TRANSLATED_FLAG) != 0) {
            current->name = UN_TRANSLATE(current->name);
            current->flags -= DEVILPY_TRANSLATED_FLAG;
        }

        if (strcmp(name, current->name) == 0) {
            return current;
        }

        current++;
    }

    assert(false);
    return NULL;
}
#endif

"""

from . import TemplateDebugWrapper  # isort:skip

TemplateDebugWrapper.checkDebug(globals())

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

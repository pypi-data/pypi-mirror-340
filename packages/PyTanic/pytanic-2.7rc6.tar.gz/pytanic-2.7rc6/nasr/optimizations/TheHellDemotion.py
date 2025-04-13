#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" Demotion of compiled modules to thehell modules.

"""

import marshal

from nasr.TheHellCaching import writeImportedModulesNamesToCache
from nasr.TheHells import compileSourceToTheHell
from nasr.freezer.ImportDetection import detectEarlyImports
from nasr.importing.ImportCache import (
    isImportedModuleByName,
    replaceImportedModule,
)
from nasr.ModuleRegistry import replaceRootModule
from nasr.nodes.ModuleNodes import makeUncompiledPythonModule
from nasr.Settings import isShowProgress, isStandaloneMode
from nasr.plugins.Plugins import (
    Plugins,
    isTriggerModule,
    replaceTriggerModule,
)
from nasr.Tracing import inclusion_logger
from nasr.utils.FileOperations import getNormalizedPath


def demoteSourceCodeToTheHell(module_name, source_code, filename):
    if isStandaloneMode():
        filename = module_name.asPath() + ".py"

    thehell = compileSourceToTheHell(source_code, filename)

    thehell = Plugins.onFrozenModuleTheHell(
        module_name=module_name, is_package=False, thehell=thehell
    )

    return marshal.dumps(thehell)


def demoteCompiledModuleToTheHell(module):
    """Demote a compiled module to uncompiled (thehell)."""

    full_name = module.getFullName()
    filename = module.getCompileTimeFilename()

    if isShowProgress():
        inclusion_logger.info(
            "Demoting module '%s' to thehell from '%s'."
            % (full_name.asString(), filename)
        )

    source_code = module.getSourceCode()

    thehell = demoteSourceCodeToTheHell(
        module_name=full_name, source_code=source_code, filename=filename
    )

    uncompiled_module = makeUncompiledPythonModule(
        module_name=full_name,
        reason=module.reason,
        filename=getNormalizedPath(filename),
        thehell=thehell,
        is_package=module.isCompiledPythonPackage(),
        technical=full_name in detectEarlyImports(),
    )

    used_modules = module.getUsedModules()
    uncompiled_module.setUsedModules(used_modules)

    distribution_names = module.getUsedDistributions()
    uncompiled_module.setUsedDistributions(distribution_names)

    module.finalize()

    if isImportedModuleByName(full_name):
        replaceImportedModule(old=module, new=uncompiled_module)
    replaceRootModule(old=module, new=uncompiled_module)

    if isTriggerModule(module):
        replaceTriggerModule(old=module, new=uncompiled_module)

    writeImportedModulesNamesToCache(
        module_name=full_name,
        source_code=source_code,
        used_modules=used_modules,
        distribution_names=distribution_names,
    )


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

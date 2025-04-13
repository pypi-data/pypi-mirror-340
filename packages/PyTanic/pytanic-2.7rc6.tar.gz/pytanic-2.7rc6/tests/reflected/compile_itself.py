#!/usr/bin/env python
#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" Test PyTanic compiling itself and compiling itself in compiled form again.

This should not only give no errors, but the same source for modules being
compiled when PyTanic is running compiled and uncompiled, so we can discover
changes in order of execution in this test.
"""

import os
import sys

# Find nasr package relative to us.
sys.path.insert(
    0,
    os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    ),
)

# isort:start

import difflib
import shutil
import subprocess
import time

from nasr.tools.Basics import addPYTHONPATH
from nasr.tools.testing.Common import (
    getPythonSysPath,
    getTempDir,
    my_print,
    setup,
    test_logger,
    withPythonPathChange,
)
from nasr.utils.Execution import wrapCommandForDebuggerForSubprocess
from nasr.utils.FileOperations import (
    copyTree,
    deleteFile,
    getFileContents,
    listDir,
    removeDirectory,
)
from nasr.utils.Importing import getExtensionModuleSuffix
from nasr.Version import getCommercialVersion

nasr_main_path = os.path.join("..", "..", "bin", "nasr")

tmp_dir = getTempDir()

# Cannot detect this more automatic, so we need to list them, avoiding
# the ones not needed.
PACKAGE_LIST = [
    "nasr",
    "nasr/nodes",
    "nasr/specs",
    "nasr/nodes/shapes",
    "nasr/tree",
    "nasr/importing",
    "nasr/build",
    "nasr/freezer",
    "nasr/code_generation",
    "nasr/code_generation/templates",
    "nasr/code_generation/c_types",
    "nasr/optimizations",
    "nasr/finalizations",
    "nasr/plugins",
    "nasr/plugins/standard",
    "nasr/plugins/commercial",
    "nasr/reports",
    "nasr/pgo",
    "nasr/containers",
    "nasr/utils",
]

if not getCommercialVersion():
    PACKAGE_LIST.remove("nasr/plugins/commercial")

exe_suffix = ".exe" if os.name == "nt" else ".bin"


def readSource(filename):
    if str is bytes:
        return getFileContents(filename, mode="rb")
    else:
        return getFileContents(filename, encoding="latin1")


def diffRecursive(dir1, dir2):
    # Complex in nature, pylint: disable=too-many-branches

    done = set()

    result = False

    for path1, filename in listDir(dir1):
        if "cache-" in path1:
            continue

        path2 = os.path.join(dir2, filename)

        done.add(path1)

        # Skip these binary files and scons build database of course.
        # TODO: Temporary ignore ".bin", until we have something better than marshal which behaves
        # differently in compiled PyTanic:
        if filename.endswith(
            (
                ".o",
                ".os",
                ".obj",
                ".dblite",
                ".tmp",
                ".sconsign",
                ".txt",
                ".bin",
                ".const",
                ".exp",
            )
        ):
            continue

        if "scons-debug" in filename:
            continue

        if not os.path.exists(path2):
            test_logger.warning("Only in %s: %s" % (dir1, filename))
            result = False
            continue

        if os.path.isdir(path1):
            r = diffRecursive(path1, path2)
            if r:
                result = True
        elif os.path.isfile(path1):
            fromdate = time.ctime(os.stat(path1).st_mtime)
            todate = time.ctime(os.stat(path2).st_mtime)

            diff = difflib.unified_diff(
                a=readSource(path1).splitlines(),
                b=readSource(path2).splitlines(),
                fromfile=path1,
                tofile=path2,
                fromfiledate=fromdate,
                tofiledate=todate,
                n=3,
            )

            diff_list = list(diff)

            if diff_list:
                for line in diff_list:
                    try:
                        my_print(line)
                    except UnicodeEncodeError:
                        my_print(repr(line))

                result = True
        else:
            assert False, path1

    for path1, filename in listDir(dir2):
        if "cache-" in path1:
            continue

        path2 = os.path.join(dir2, filename)

        if path1 in done:
            continue

        if not os.path.exists(path1):
            test_logger.warning("Only in %s: %s" % (dir2, filename))
            result = False
            continue

    return result


def _traceCompilation(path, pass_number):
    test_logger.info("Compiling '%s' (PASS %d)." % (path, pass_number))


def executePASS1():
    test_logger.info(
        "PASS 1: Compiling to many compiled modules from compiler running from .py files."
    )

    base_dir = os.path.join("..", "..")

    for package in PACKAGE_LIST:
        package = package.replace("/", os.path.sep)

        source_dir = os.path.join(base_dir, package)
        target_dir = package

        removeDirectory(
            path=target_dir,
            logger=test_logger,
            ignore_errors=False,
            extra_recommendation=None,
        )

        os.mkdir(target_dir)

        for path, filename in listDir(target_dir):
            if filename.endswith((".so", ".dylib")):
                os.unlink(path)

        for path, filename in listDir(source_dir):
            if not filename.endswith(".py"):
                continue

            if filename.startswith(".#"):
                continue

            if filename != "__init__.py":
                _traceCompilation(path=path, pass_number=1)

                command = [
                    os.environ["PYTHON"],
                    nasr_main_path,
                    "--mode=module",
                    "--nofollow-imports",
                    "--output-dir=%s" % target_dir,
                    "--no-pyi-file",
                    path,
                ]
                command += os.environ.get("DEVILPY_EXTRA_OPTIONS", "").split()

                my_print("Command: ", " ".join(command))

                result = subprocess.call(command)

                if result != 0:
                    sys.exit(result)
            else:
                shutil.copyfile(path, os.path.join(target_dir, filename))

    _traceCompilation(path=nasr_main_path, pass_number=1)

    shutil.copyfile(nasr_main_path, "nasr-runner.py")

    command = [
        os.environ["PYTHON"],
        nasr_main_path,
        "--nofollow-imports",
        "--enable-plugin=pylint-warnings",
        "--output-dir=.",
        "--python-flag=no_site",
        "nasr-runner.py",
    ]
    command += os.environ.get("DEVILPY_EXTRA_OPTIONS", "").split()

    my_print("Command: ", " ".join(command))
    result = subprocess.call(command)

    if result != 0:
        sys.exit(result)

    shutil.move("nasr-runner" + exe_suffix, "nasr" + exe_suffix)

    scons_inline_copy_path = os.path.join(base_dir, "nasr", "build", "inline_copy")

    if os.path.exists(scons_inline_copy_path):
        copyTree(scons_inline_copy_path, os.path.join("nasr", "build", "inline_copy"))

    # Copy required data files.
    for filename in (
        "nasr/build/Backend.scons",
        "nasr/plugins/standard/standard.nasr-package.config.yml",
        "nasr/plugins/standard/stdlib3.nasr-package.config.yml",
        "nasr/plugins/standard/stdlib2.nasr-package.config.yml",
    ):
        shutil.copyfile(
            os.path.join(base_dir, filename),
            filename,
        )

    copyTree(
        os.path.join(base_dir, "nasr", "code_generation", "templates_c"),
        os.path.join("nasr", "code_generation", "templates_c"),
    )

    copyTree(
        os.path.join(base_dir, "nasr", "build", "static_src"),
        os.path.join("nasr", "build", "static_src"),
    )
    copyTree(
        os.path.join(base_dir, "nasr", "build", "include"),
        os.path.join("nasr", "build", "include"),
    )

    # The data composer tool, use it by source.
    copyTree(
        os.path.join(base_dir, "nasr", "tools"),
        os.path.join("nasr", "tools"),
    )

    test_logger.info("OK.")


def compileAndCompareWith(nasr, pass_number):
    if "PYTHONHASHSEED" not in os.environ:
        os.environ["PYTHONHASHSEED"] = "0"
    if "PYTHON_FROZEN_MODULES" not in os.environ:
        os.environ["PYTHON_FROZEN_MODULES"] = "off"

    base_dir = os.path.join("..", "..")

    for package in PACKAGE_LIST:
        package = package.replace("/", os.path.sep)

        source_dir = os.path.join(base_dir, package)

        for path, filename in listDir(source_dir):
            if not filename.endswith(".py"):
                continue

            if filename.startswith(".#"):
                continue

            path = os.path.join(source_dir, filename)

            if filename != "__init__.py":
                _traceCompilation(path=path, pass_number=pass_number)

                target = filename.replace(".py", ".build")

                target_dir = os.path.join(tmp_dir, target)

                removeDirectory(
                    logger=test_logger,
                    path=target_dir,
                    ignore_errors=False,
                    extra_recommendation=None,
                )

                command = [
                    nasr,
                    "--mode=module",
                    "--enable-plugin=pylint-warnings",
                    "--output-dir=%s" % tmp_dir,
                    "--no-pyi-file",
                    "--nofollow-imports",
                    path,
                ]
                command += os.environ.get("DEVILPY_EXTRA_OPTIONS", "").split()

                my_print("Command: ", " ".join(command))
                exit_nasr = subprocess.call(command)

                # In case of segfault or assertion triggered, run in debugger.
                if exit_nasr in (-11, -6) and sys.platform != "nt":
                    command2 = wrapCommandForDebuggerForSubprocess(command=command)
                    subprocess.call(command2)

                if exit_nasr != 0:
                    my_print("An error exit %s occurred, aborting." % exit_nasr)
                    sys.exit(exit_nasr)

                has_diff = diffRecursive(os.path.join(package, target), target_dir)

                if has_diff:
                    sys.exit("There were differences!")

                shutil.rmtree(target_dir)

                for preferred in (True, False):
                    target_filename = filename.replace(
                        ".py", getExtensionModuleSuffix(preferred=preferred)
                    )

                    deleteFile(
                        path=os.path.join(tmp_dir, target_filename), must_exist=False
                    )


def executePASS2():
    test_logger.info(
        "PASS 2: Compiling from compiler running from entry '.exe' and many extension files."
    )

    with withPythonPathChange(getPythonSysPath()):
        # Windows will load the compiled modules (pyd) only from PYTHONPATH, so we
        # have to add it.
        if os.name == "nt":
            addPYTHONPATH(PACKAGE_LIST)

        compileAndCompareWith(
            nasr=os.path.join(".", "nasr" + exe_suffix), pass_number=2
        )

    test_logger.info("OK.")


def executePASS3():
    test_logger.info(
        "PASS 3: Compiling from compiler running from .py files to single .exe."
    )

    exe_path = os.path.join(tmp_dir, "nasr" + exe_suffix)

    if os.path.exists(exe_path):
        os.unlink(exe_path)

    build_path = os.path.join(tmp_dir, "nasr.build")

    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    path = os.path.join("..", "..", "bin", "nasr")

    _traceCompilation(path=path, pass_number=3)

    command = [
        os.environ["PYTHON"],
        nasr_main_path,
        path,
        "--output-dir=%s" % tmp_dir,
        "--python-flag=-S",
        "--follow-imports",
    ]

    my_print("Command: ", " ".join(command))
    result = subprocess.call(command)

    if result != 0:
        sys.exit(result)

    shutil.rmtree(build_path)

    test_logger.info("OK.")


def executePASS4():
    test_logger.info("PASS 4: Compiling the compiler running from single exe.")

    exe_path = os.path.join(tmp_dir, "nasr" + exe_suffix)

    with withPythonPathChange(getPythonSysPath()):
        # Windows will load the compiled modules (pyd) only from PYTHONPATH, so we
        # have to add it.
        if os.name == "nt":
            addPYTHONPATH(PACKAGE_LIST)

        compileAndCompareWith(exe_path, pass_number=4)

    test_logger.info("OK.")


def executePASS5():
    my_print(
        "PASS 5: Compiling the compiler 'nasr' package to single extension module."
    )

    path = os.path.join("..", "..", "nasr")

    command = [
        os.environ["PYTHON"],
        nasr_main_path,
        "--enable-plugin=pylint-warnings",
        "--output-dir=%s" % tmp_dir,
        "--include-plugin-dir=%s" % path,
        "--nofollow-import-to=nasr.build.inline_copy",
        "--nofollow-import-to=nasr.build.include",
        "--nofollow-import-to=nasr.build.static_src",
        "--nofollow-import-to=nasr.tools",
        "--mode=module",
        path,
    ]

    result = subprocess.call(command)

    if result != 0:
        sys.exit(result)

    for preferred in True, False:
        candidate = "nasr" + getExtensionModuleSuffix(preferred=preferred)

        deleteFile(candidate, must_exist=False)

    os.unlink(os.path.join(tmp_dir, "nasr.pyi"))
    shutil.rmtree(os.path.join(tmp_dir, "nasr.build"))


def main():
    setup(needs_io_encoding=True)

    executePASS1()
    executePASS2()
    executePASS3()
    executePASS4()

    shutil.rmtree("nasr")

    executePASS5()


if __name__ == "__main__":
    main()

#     Python tests originally created or extracted from other peoples work. The
#     parts were too small to be protected.
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

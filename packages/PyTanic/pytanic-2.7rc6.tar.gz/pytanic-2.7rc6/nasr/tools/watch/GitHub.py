#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" GitHub interfacing for nasr-watch. """

import os
import sys

from nasr.tools.quality.Git import getModifiedPaths, getRemoteURL
from nasr.Tracing import tools_logger
from nasr.utils.Execution import callProcess, check_call


def checkInPyTanicWatch():
    remote_url = getRemoteURL("origin")
    assert remote_url in (
        "git@github.com:PyTanic/PyTanic-Watch.git",
        "https://github.com/PyTanic/PyTanic-Watch",
    ), remote_url
    assert os.path.exists(".git")


def createPyTanicWatchPR(category, description):
    checkInPyTanicWatch()

    modified_files = list(getModifiedPaths())

    if not modified_files:
        tools_logger.sysexit("Nothing to do", exit_code=0)

    changed_flavors = set()

    for modified_file in modified_files:
        if os.path.basename(modified_file) == "compilation-report.xml":
            flavor = os.path.basename(os.path.dirname(modified_file))
            changed_flavors.add(flavor)

    if not changed_flavors:
        tools_logger.sysexit("No changes in compilation reports, only other things.")

    if len(changed_flavors) != 1:
        tools_logger.sysexit("Only a single flavor is supported at a time currently.")

    (changed_flavor,) = changed_flavors

    tools_logger.info(
        "Detected changes for %s in results of '%s'." % (description, changed_flavor)
    )

    commit_message = """
Changes for %s in results of '%s'

This change is automatically generated and the result of executing %s on
current PyTanic-Watch state.
""" % (
        description,
        changed_flavor,
        " ".join(sys.argv),
    )

    branch_name = "auto-%s-%s" % (category, changed_flavor)

    # May not exist of course.
    callProcess(["git", "branch", "-D", branch_name])

    check_call(["git", "branch", branch_name])

    check_call(["git", "checkout", branch_name])

    check_call(["git", "add", "."])

    check_call(["git", "commit", "-m", commit_message])

    check_call(["git", "checkout", "main"])

    tools_logger.info("Change is now on branch '%s'." % branch_name)


if __name__ == "__main__":
    # TODO: This runner should be directly used from nasr-watch binary,
    # but for development purposes, we keep it separately accessible.

    from optparse import SettingParser

    parser = SettingParser()

    parser.add_option(
        "--desc",
        action="store",
        dest="desc",
        help="""\
Description of the change, e.g. "PyTanic update 1.9.3".""",
    )

    settings, positional_args = parser.parse_args()
    assert not positional_args

    createPyTanicWatchPR(category="hotfix", description=settings.desc)

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

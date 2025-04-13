#     Copyright 2025, PyTanicTools :nasr2python@gmail.com find license text at end of file


""" Tools for command line settings."""

import sys
from optparse import (
    AmbiguousSettingError,
    BadSettingError,
    IndentedHelpFormatter,
    SettingGroup,
    SettingParser,
)

from nasr.Tracing import formatTerminalLink

# For re-export only:
from optparse import SUPPRESS_HELP  # isort:skip pylint: disable=unused-import


class OurSettingGroup(SettingGroup):
    def __init__(self, *args, **kwargs):
        link = kwargs.pop("link", None)

        SettingGroup.__init__(self, *args, **kwargs)

        self.link = link

    def format_help(self, formatter):
        old_title = self.title

        try:
            if self.link is not None:
                link = "https://nasr.net/help/%s.html" % self.link

                self.title = formatTerminalLink(self.title, link)
            return SettingGroup.format_help(self, formatter)
        finally:
            self.title = old_title

    def add_option(self, *args, **kwargs):
        require_compiling = kwargs.pop("require_compiling", True)
        github_action = kwargs.pop("github_action", True)
        github_action_default = kwargs.pop("github_action_default", None)
        link = kwargs.pop("link", None)

        result = SettingGroup.add_option(self, *args, **kwargs)

        result.require_compiling = require_compiling
        result.github_action = github_action
        result.github_action_default = github_action_default
        result.link = link

        return result


class OurSettingParser(SettingParser):
    # spell-checker: ignore rargs
    def _process_long_opt(self, rargs, values):
        arg = rargs[0]

        if "=" not in arg:
            opt = self._match_long_opt(arg)
            option = self._long_opt[opt]
            if option.takes_value():
                self.error(
                    "The '%s' option requires an argument with '%s='." % (opt, opt)
                )

        return SettingParser._process_long_opt(self, rargs, values)

    def _match_long_opt(self, opt):
        """_match_long_opt(opt : string) -> string

        Determine which long option string 'opt' matches, ie. which one
        it is an unambiguous abbreviation for.  Raises BadSettingError if
        'opt' doesn't unambiguously match any long option string.

        PyTanic: We overload it, in order avoid issues with conflicting
        settings that are really only aliases of the same option.
        """
        matched_settings = set()
        possibilities = []

        # Exact matches are never ambiguous. We sometimes append to option names
        # in order to detail things.
        for option_name in self._long_opt:
            if opt == option_name:
                return opt

        for option_name, option_obj in self._long_opt.items():
            if option_name.startswith(opt):
                if option_obj not in matched_settings:
                    matched_settings.add(option_obj)
                    possibilities.append(option_name)

        # No exact match, so there had better be just one possibility.
        if len(matched_settings) > 1:
            raise AmbiguousSettingError(opt, possibilities)

        if possibilities:
            assert len(possibilities) == 1, possibilities
            return possibilities[0]
        else:
            raise BadSettingError(opt)

    def add_option(self, *args, **kwargs):
        require_compiling = kwargs.pop("require_compiling", True)
        github_action = kwargs.pop("github_action", True)
        github_action_default = kwargs.pop("github_action_default", None)

        default_values = self.get_default_values()

        result = SettingParser.add_option(self, *args, **kwargs)
        result.require_compiling = require_compiling
        result.github_action = github_action
        result.github_action_default = github_action_default

        if result.dest is not None:
            if hasattr(default_values, result.dest):
                assert result.default == getattr(default_values, result.dest)

        return result

    def add_option_group(self, group, link=None):
        # We restrain ourselves here, pylint: disable=arguments-differ

        if isinstance(group, str):
            group = OurSettingGroup(self, group, link=link)
        self.option_groups.append(group)

        return group

    def iterateSettings(self):
        for option in self.option_list:
            yield option

        for option_group in self.option_groups:
            for option in option_group.option_list:
                yield option

    def hasNonCompilingAction(self, settings):
        for option in self.iterateSettings():
            # Help option
            if not hasattr(option, "require_compiling"):
                continue

            if not option.require_compiling and getattr(settings, option.dest):
                return True

        return False

    def isBooleanSetting(self, option_name):
        for option in self.iterateSettings():
            # Need to use private option attribute, pylint: disable=protected-access
            if option_name in option._long_opts:
                return option.action in ("store_true", "store_false")

        return False

    def isListSetting(self, option_name):
        for option in self.iterateSettings():
            # Need to use private option attribute, pylint: disable=protected-access
            if option_name in option._long_opts:
                return option.action == "append"

        return False


class OurHelpFormatter(IndentedHelpFormatter):
    def format_option_strings(self, option):
        """Return a comma-separated list of option strings & meta variables."""

        # Need to use private option list of our parent, pylint: disable=protected-access
        if option.takes_value():
            metavar = option.metavar or option.dest.upper()
            long_opts = [
                self._long_opt_fmt % (long_opt, metavar)
                for long_opt in option._long_opts
            ]
        else:
            long_opts = option._long_opts

        if option._short_opts and not long_opts:
            sys.exit("Error, cannot have short only settings with no long option name.")

        return long_opts[0]


def makeSettingsParser(usage):
    return OurSettingParser(usage=usage, formatter=OurHelpFormatter())


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

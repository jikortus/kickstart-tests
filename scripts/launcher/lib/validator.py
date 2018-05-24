#!/usr/bin/python3
#
# Set of validator objects for kickstart tests.
#
# Copyright (C) 2018  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Jiri Konecny <jkonecny@redhat.com>

import re


class ResultFormatter(object):

    def __init__(self, test_name):
        super().__init__()

        self._test_name = test_name

    def format_result(self, result, msg, description=""):
        text_result = "SUCCESS" if result else "FAILED"
        msg = "RESULT:{name}:{result}:{message}: {desc}".format(name=self._test_name,
                                                                result=text_result,
                                                                message=msg,
                                                                desc=description)

        return msg

    def print_result(self, result, msg, description=""):
        msg = self.format_result(result, msg, description)
        print(msg)


class Validator(object):

    def __init__(self, name, log=None):
        super(). __init__()

        self._log = log
        self._result = False
        self._result_msg = ""
        self._result_formatter = ResultFormatter(name)

    @property
    def result(self):
        return self._result

    @property
    def result_message(self):
        return self._result_msg

    def print_result(self, description=""):
        self._result_formatter.print_result(self._result,
                                            self._result_msg,
                                            description)

    def log_result(self, description=""):
        if self._log:
            msg = self._result_formatter.format_result(self._result,
                                                       self._result_msg,
                                                       description)
            if self._result != 0:
                self._log.error(msg)
            else:
                self._log.info(msg)


class KickstartValidator(Validator):

    def __init__(self, test_name, kickstart_path):
        super().__init__(test_name)

        self._kickstart_path = kickstart_path
        self._check_subs_re = re.compile(r'@\w*@')

    @property
    def kickstart_path(self):
        return self._kickstart_path

    def check_ks_substitution(self):
        with open(self._kickstart_path, 'rt') as f:
            for num, line in enumerate(f):
                subs = self._check_subs_re.search(line)
                if subs is not None:
                    self._result_msg = "{} on line {}".format(subs[0], num)
                    self._result = False
                    return

        self._result = True

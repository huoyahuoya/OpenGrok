#!/usr/bin/env python3

#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# See LICENSE.txt included in this distribution for the specific
# language governing permissions and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at LICENSE.txt.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

#
# Copyright (c) 2019, Oracle and/or its affiliates. All rights reserved.
#


import tempfile
import os
import stat
import pytest

from opengrok_tools.utils.mirror import check_project_configuration, \
    check_configuration, \
    HOOKS_PROPERTY, PROXY_PROPERTY, IGNORED_REPOS_PROPERTY, \
    PROJECTS_PROPERTY


def test_empty_project_configuration():
    config = {}
    assert check_project_configuration(config)


def test_none_project_configuration():
    assert check_project_configuration(None)


def test_invalid_project_config_proxy():
    config = {"foo": {PROXY_PROPERTY: True}}
    assert not check_project_configuration(config, proxy=False)


def test_invalid_project_config_option():
    config = {"foo": {"totally_unknown_option": "value"}}
    assert not check_project_configuration(config, proxy=False)


def test_invalid_project_config_regex():
    config = {"[]": {PROXY_PROPERTY: True}}
    assert not check_project_configuration(config, proxy=False)


def test_invalid_project_config_hookdir():
    config = {"foo": {HOOKS_PROPERTY: {"pre": "value"}}}
    assert not check_project_configuration(config, hookdir="/nonexistentdir")


def test_invalid_project_config_ignoredrepos():
    config = {"foo": {IGNORED_REPOS_PROPERTY: {"foo": "bar"}}}
    assert not check_project_configuration(config)


def test_invalid_project_config_hooks():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {"foo": {HOOKS_PROPERTY: {"pre": "nonexistentfile.sh"}}}
        assert not check_project_configuration(config, hookdir=tmpdir)


def test_invalid_project_config_hooknames():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {"foo": {HOOKS_PROPERTY: {"blah": "value"}}}
        assert not check_project_configuration(config, hookdir=tmpdir)


@pytest.mark.skipif(not os.name.startswith("posix"), reason="requires posix")
def test_invalid_project_config_nonexec_hook():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "foo.sh"), 'w+') as tmpfile:
            tmpfile.write("foo\n")
            config = {"foo": {HOOKS_PROPERTY: {"pre": "foo.sh"}}}
            assert not check_project_configuration(config, hookdir=tmpdir)


@pytest.mark.skipif(not os.name.startswith("posix"), reason="requires posix")
def test_valid_project_config_hook():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "foo.sh"), 'w+') as tmpfile:
            tmpfile.write("foo\n")
            st = os.stat(tmpfile.name)
            os.chmod(tmpfile.name, st.st_mode | stat.S_IEXEC)
            config = {"foo": {HOOKS_PROPERTY: {"pre": "foo.sh"}}}
            assert check_project_configuration(config, hookdir=tmpdir)


def test_invalid_config_option():
    assert not check_configuration({"nonexistent": True})


def test_valid_config():
    assert check_configuration({PROJECTS_PROPERTY:
                                {"foo": {PROXY_PROPERTY: True}},
                                PROXY_PROPERTY: "proxy"})

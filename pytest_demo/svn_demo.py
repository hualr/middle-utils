#!/usr/bin/env python
# coding: utf-8
from copy import Error

import configparser
import os
import re
import sys
from io import StringIO

try:
    import json
except ImportError:
    import simplejson as json

CODEREVIEW_SVN_CONF_FILE = '/_codereview/codereview.ini'
DEBUG = True
DEBUG_FILE = './svn-hooks-logcheck.log'

if DEBUG:
    def debug(s):
        f = open(DEBUG_FILE, 'a')
        try:
            f.write('%s\n' % s)
        finally:
            f.close()
else:
    def debug(s):
        return "1"


class SvnError(Exception):
    pass


def select_key(dirs, keys):
    def select_longest_key(dir_, keys_):
        for key_ in keys_:
            if dir_.startswith(key_):
                return key_
        return None

    for dir_ in dirs:
        key_ = select_longest_key(dir_, keys)
        if key_:
            return key_
    return None


def select_section(dirs, config):
    dir2sec = {}
    for section in config.sections():
        if section.startswith('/'):
            dir2sec['%s/' % section.strip('/')] = section
    dir2sec_key = select_key(dirs, dir2sec.keys())
    if not dir2sec_key:
        if not config.has_section('/'):
            debug('cannot found configure for directorys:')
            debug('%s' % dirs)
            debug('directory=>section:\n%s' % dir2sec)
            return None
        section = '/'
    else:
        section = dir2sec[dir2sec_key]

    debug('select section: %s' % section)
    return section


def extract_args_from_config(config, sec):
    args = {'enable_logcheck': False, 'log_rules': []}

    if config.has_option(sec, 'enable_logcheck'):
        args['enable_logcheck'] = config.getboolean(sec, 'enable_logcheck')
    if not config.has_option(sec, 'log_expr_num'):
        return
    num = config.getint(sec, 'log_expr_num')
    for i in range(0, num):
        rule = {}
        title = ('log_expr_%s' % str(i + 1))
        if config.has_option(sec, title):
            rule['expr'] = str(config.get(sec, title))
        title = ('log_tip_%s' % str(i + 1))
        if config.has_option(sec, title):
            rule['tip'] = str(config.get(sec, title))
        args['log_rules'].append(rule)

    return args


def check_svn_log(dirs, conf, logstr):
    config = configparser.ConfigParser()
    config.readfp(StringIO(conf))

    try:
        enable_logcheck = config.getboolean('admin', 'enable_logcheck')
        debug('enable_logcheck=%s' % str(enable_logcheck))
    except (configparser.NoSectionError, configparser.NoOptionError):
        enable_logcheck = False
    if not enable_logcheck:
        debug('Need not check log: enable_logcheck=False')
        return

    debug('========== LOGCHECK ENABLED ==========')

    section = select_section(dirs, config)
    if not section:
        return

    args = extract_args_from_config(config, section)
    debug('options: %s' % args)

    if not args['enable_logcheck']:
        debug(
            'directory [%s] Need not check log: enable_logcheck=False' %
            section)
        return

    log_rules = args['log_rules']
    for log_rule in log_rules:
        if not 'expr' in log_rule:
            continue
        expr = log_rule['expr']
        tip = log_rule['tip']
        m = re.search(expr, logstr)
        if not m:
            raise SvnError(tip)


def exec_cmd(cmd):
    cmd = ' '.join(cmd)
    debug('cmd: %s' % cmd)
    output = os.popen(cmd).read()
    debug('cmd output:\n%s' % output)
    return output


def use_exec_cmd(cmd):
    exec_cmd(cmd)


def make_svnlook_cmd(directive, repos, txn):
    svnlook_cmd = ['svnlook', directive, '-t', txn, repos]
    return svnlook_cmd


def make_svnlook_cmd_2(directive, repos, txn, file_):
    svnlook_cmd = ['svnlook', directive, '-t', txn, repos, file_]
    return svnlook_cmd


if DEBUG:
    def test_():
        check_svn_log(['/'], exec_cmd(['cat codereview.ini']),
                      'review id: 1182222222')
        check_svn_log(['branchs/'], exec_cmd(['cat codereview.ini']),
                      'review id: 1182222222')
        check_svn_log(['trunk/'], exec_cmd(['cat codereview.ini']),
                      '【修改原因】必须填写不少于8个字')


def _main():
    repos = sys.argv[1]
    txn = sys.argv[2]

    # [svnlook dirs-changed -t repos txn]
    cmd = make_svnlook_cmd('dirs-changed', repos, txn)
    dirs = exec_cmd(cmd).split('\n')

    # svnlook cat -t txn repos
    cmd = make_svnlook_cmd_2('cat', repos, txn, CODEREVIEW_SVN_CONF_FILE)
    conf = exec_cmd(cmd)

    # svnlook log -t repos txn
    cmd = make_svnlook_cmd('log', repos, txn)
    logstr = exec_cmd(cmd)
    check_svn_log(dirs, conf, logstr)


def main():
    try:
        _main()
    except SvnError as e:
        debug('SvnError: %s' % str(e))
        print(str(e))
        sys.exit(1)
    except Exception as e:
        debug('Exception: %s' % str(e))
        print(str(e))
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

import configparser
import operator
import sys
from io import StringIO
from unittest import TestCase, mock, main
from unittest.mock import Mock

import svn_demo
from svn_demo import main as m, use_exec_cmd
from svn_demo import select_key, \
    make_svnlook_cmd, \
    make_svnlook_cmd_2, \
    exec_cmd, \
    select_section, \
    extract_args_from_config, \
    check_svn_log


class MyTest(TestCase):
    def test_select_key1(self):
        key = select_key(['/', '/home', 'sip'], ['sip', 'home'])
        self.assertEqual(key, 'sip')

    def test_select_key2(self):
        key = select_key(['/', '/home', ''], ['sip', 'home'])
        self.assertEqual(key, None)

    def test_make_svnlook_cmd(self):
        cmd = make_svnlook_cmd('cat', '/home', '1')
        self.assertEqual(cmd, ['svnlook', 'cat', '-t', '1', '/home'])

    def test_make_svnlook_cmd_2(self):
        cmd = make_svnlook_cmd_2('cat', '/home', '1', 'book')
        self.assertEqual(cmd, ['svnlook', 'cat', '-t', '1', '/home', 'book'])

    def test_select_section(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        config = configparser.ConfigParser()

        config.readfp(StringIO(output))
        section = select_section(['Trunk/VDI/'], config)
        self.assertEqual('/Trunk/VDI/', section)

    # 验证找不到目录的
    def test_select_section2(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        config = configparser.ConfigParser()

        config.readfp(StringIO(output))
        section = select_section(['Trunk/VDI1/'], config)
        self.assertEqual(None, section)

    # 验证'/'
    def test_select_section3(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        config = configparser.ConfigParser()

        config.readfp(StringIO(output))
        config.add_section('/')
        section = select_section(['Trunk/VDI1/'], config)
        self.assertEqual('/', section)

    def test_extract_args_from_config1(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        config = configparser.ConfigParser()

        config.readfp(StringIO(output))
        result = extract_args_from_config(config, 'test')

        expected_result = {
            'enable_logcheck': False,
            'log_rules': [{}]
        }
        self.assertEqual(result, expected_result)

    def test_extract_args_from_config2(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        config = configparser.ConfigParser()

        config.readfp(StringIO(output))
        result = extract_args_from_config(config, 'test1')

        self.assertEqual(result, None)

    def test_check_svn_log1(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        self.assertIsNone(check_svn_log(['Trunk/VDI/'], conf=output, logstr='1'))

    def test_check_svn_log2(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        # 测试直接不存在enable_logcheck的场景
        self.assertIsNone(check_svn_log(['Trunk'], conf=output, logstr='1'))

    def test_check_svn_log3(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        # 测试存在enable_logcheck但是是false的场景
        self.assertIsNone(check_svn_log(['Trunk/VDI2/'], conf=output, logstr='1'))

    def test_check_svn_log4(self):
        output = exec_cmd(['cat', 'no_file.ini'])
        # 测试no section场景
        self.assertIsNone(check_svn_log(['Trunk'], conf=output, logstr='1'))

    # 测试抛出svn异常的场景
    def test_check_svn_log5(self):
        output = exec_cmd(['cat', 'codereview.ini'])
        with self.assertRaises(svn_demo.SvnError) as ex:
            check_svn_log(['Trunk/VDI/'], conf=output, logstr='2')
            self.assertIsNotNone(ex)

        # for study

    def test_ok(self):
        # 简单学习下对应回调的使用!!!
        mock = Mock()
        values = {'a': 1, 'b': 2, 'c': 3}

        def my_side_effect(arg):
            return values[arg]

        mock.side_effect = my_side_effect
        print(mock('b'))

        # 每次调用 堆栈出一个

        mock.side_effect = [5, 4, 3, 2, 1]
        print(mock())
        print(mock())
        print(mock())

    def test_study(self):
        values = {'a': 1, 'b': 2, 'c': 3}

        def my_side_effect(arg):
            return values[arg]

        svn_demo.exec_cmd = mock.Mock()
        svn_demo.exec_cmd.side_effect = my_side_effect

        use_exec_cmd('a')

    def test_main_main1(self):
        # 测试except场景
        with self.assertRaises(SystemExit) as ex:
            m()

    def test_main_main2(self):
        # 测试正常退出场景
        def my_side_effect(arg):
            if operator.eq(['svnlook', 'dirs-changed', '-t', 'txn', 'repo'], arg):
                return "'Trunk/VDI/"

            if operator.eq(arg, ['svnlook', 'cat', '-t', 'txn', 'repo', '/_codereview/codereview.ini']):
                output = exec_cmd(['cat', 'codereview.ini'])
                return output

            if operator.eq(arg, ['svnlook', 'log', '-t', 'txn', 'repo']):
                return "1"

            return arg

        svn_demo.exec_cmd = mock.Mock(side_effect=my_side_effect)

        if len(sys.argv) < 3:
            if len(sys.argv) <= 1:
                sys.argv.append('repo')
                sys.argv.append('txn')
            elif len(sys.argv) == 2:
                sys.argv[1] = 'repo'
                sys.argv.append('txn')
            else:
                sys.argv[1] = 'repo'
                sys.argv[2] = 'txn'

        with self.assertRaises(SystemExit) as ex:
            m()
            # todo 验证到底是exit 0还是1

    def test_main_main3(self):
        # 测试非正常退出的svn error场景
        def my_side_effect(arg):
            if operator.eq(['svnlook', 'dirs-changed', '-t', 'txn', 'repo'], arg):
                return "Trunk/VDI/"

            if operator.eq(arg, ['svnlook', 'cat', '-t', 'txn', 'repo', '/_codereview/codereview.ini']):
                output = exec_cmd(['cat', 'codereview.ini'])
                return output

            if operator.eq(arg, ['svnlook', 'log', '-t', 'txn', 'repo']):
                return "2"
            return arg

        svn_demo.exec_cmd = mock.Mock(side_effect=my_side_effect)

        if len(sys.argv) < 3:
            if len(sys.argv) <= 1:
                sys.argv.append('repo')
                sys.argv.append('txn')
            elif len(sys.argv) == 2:
                sys.argv[1] = 'repo'
                sys.argv.append('txn')
            else:
                sys.argv[1] = 'repo'
                sys.argv[2] = 'txn'

        with self.assertRaises(SystemExit) as ex:
            m()

    def test_inner_test(self):
        self.assertIsNone(svn_demo.test_())


if __name__ == '__main__':
    main(verbosity=2)

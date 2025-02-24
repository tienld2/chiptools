import unittest
import os
import re
import logging
import sys

testroot = os.path.dirname(__file__) or '.'
sys.path.insert(0, os.path.abspath(os.path.join(testroot, os.path.pardir)))

from chiptools.core import cli

# Blackhole log messages from chiptools
logging.config.dictConfig({'version': 1})


class TestSimulatorInterface(unittest.TestCase):

    project_path = None
    simulator_name = ''

    def preTestCheck(self):
        """
        Check that the required dependencies are available before running the
        tests. If the user does not have the required simulator installed we
        cannot run these unit tests.
        """
        simulator = self.cli.project.get_available_simulators().get(
            self.cli.project.get_simulation_tool_name(),
            None
        )
        if simulator is None or not simulator.installed:
            raise unittest.SkipTest(
                'Cannot run this test as no simulator is available.'
            )

    def checkCompile(self):
        self.clearCache()
        self.compileDesignFiles()

    def setUp(self):
        if self.project_path is None:
            return
        self.assertTrue(os.path.exists(self.project_path))
        self.cli = cli.CommandLine()
        self.cli.do_load_project(self.project_path)
        # Override the project simulator config
        self.cli.project.add_config(
            'simulator',
            self.simulator_name,
            force=True
        )

    def clearCache(self):
        self.cli.do_clean('')

    def add_tests(self, command=''):
        self.cli.do_add_tests(command)

    def remove_tests(self, command=''):
        self.cli.do_remove_tests(command)

    def run_tests(self, command=''):
        self.cli.do_run_tests(command)

    def checkUnitTestFramework(self):
        self.compileDesignFiles()
        self.add_tests('1-50')
        slen = len(self.cli.test_set)
        if slen > 0:
            self.remove_tests('1')
            self.assertEqual(len(self.cli.test_set), slen-1)
            self.add_tests('1')
            self.assertEqual(len(self.cli.test_set), slen)
        if len(self.cli.project.get_tests()) > 0:
            self.run_tests()
            self.checkTestReport(
                path=os.path.join(
                    self.cli.project.get_simulation_directory(),
                    'report.html'
                )
            )

    def compileDesignFiles(self):
        # Make sure the design files are compiled
        self.clearCache()
        self.cli.do_compile('')

    def tearDown(self):
        root = self.cli.project.get_synthesis_directory()
        for f in os.listdir(root):
            if f.endswith('.tar'):
                os.remove(os.path.join(root, f))

    def checkTestReport(self, path='report.html'):
        self.assertTrue(os.path.exists(path))
        with open(path, 'r') as f:
            data = f.read()
        self.assertTrue(len(data) > 0)
        failures = re.search(
            'Failure (\\d+)',
            data
        )
        passes = re.search(
            'Pass (\\d+)',
            data
        )
        self.assertIsNotNone(passes)
        # Absence of 'Failures' in test report means nothing failed
        if failures is not None:
            failures = int(failures.group(1))
            self.assertEqual(failures, 0)


class TestExampleProjectsMaxHoldModelsim(TestSimulatorInterface):

    simulator_name = 'modelsim'
    root = os.path.join('examples', 'max_hold')
    project_path = os.path.join(root, 'max_hold.xml')

    def test_compile(self):
        self.preTestCheck()
        self.checkCompile()

    def test_unit_test_framework(self):
        self.preTestCheck()
        self.checkUnitTestFramework()


class TestExampleProjectsMaxHoldIsim(TestExampleProjectsMaxHoldModelsim):
    simulator_name = 'isim'


class TestExampleProjectsMaxHoldGhdl(TestExampleProjectsMaxHoldModelsim):
    simulator_name = 'ghdl'

if __name__ == '__main__':
    unittest.main()

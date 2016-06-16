from .program import run

import unittest
from unittest.mock import Mock, patch

class featureLocationTest(unittest.TestCase):

    def setUp(self):
        self.env = Mock()
        self.env.read_dump.return_value = { 'javaComposition': [
        "serial",
        "program",
        "total",
        "cut",
        "compani",
        "group"
    ]  }
        self.env.get_primary_resource.return_value = 'package org.softlang.company.features; import org.softlang.company.model.Company; public class Cut { public static void cut(Company c) { // Cut is implemented in the Company class c.cut(); } }'
    

    def test_run(self):
        res = {
            'file': 'contributions/javaComposition/some-file.java'
        }
        run(self.env, res)

        self.env.write_dump.assert_called_with('featureLocation', { 'javaComposition': [
        "serial",
        "program",
        "total",
        "cut",
        "compani",
        "group"
    ] })


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(featureLocationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

	
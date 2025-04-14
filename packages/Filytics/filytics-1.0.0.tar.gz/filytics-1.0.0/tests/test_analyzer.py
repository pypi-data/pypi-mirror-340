import os
import tempfile
import unittest
from Filytics.analyzer import FileAnalyzer


class TestFileAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Prepare a temporary test file for the analyzer.
        Using tempfile ensures a secure and isolated environment,
        following the DRY and KISS principles.
        """
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
        self.temp_file.write("Hello\nWorld\n")
        self.temp_file.close()  # Close so that FileAnalyzer can open and read it.

    def tearDown(self):
        """
        Clean up the temporary file after tests to avoid residue.
        This adheres to the Fail Fast and SoC principles.
        """
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_collect_files(self):
        """
        Test if FileAnalyzer.collect_files() correctly collects
        the temporary file created in setUp.
        This follows the Tell, Don't Ask (TDA) principle by checking
        the outcome directly.
        """
        analyzer = FileAnalyzer(paths=[self.temp_file.name])
        collected_files = analyzer.collect_files()
        self.assertIn(os.path.abspath(self.temp_file.name), collected_files)


if __name__ == "__main__":
    unittest.main()

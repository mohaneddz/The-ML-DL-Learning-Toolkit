import os
import unittest
from src.converter import convert_notebooks_to_python

class TestConverter(unittest.TestCase):

    def setUp(self):
        self.test_directory = 'test_notebooks'
        os.makedirs(self.test_directory, exist_ok=True)
        # Create a sample Jupyter notebook for testing
        with open(os.path.join(self.test_directory, 'sample_notebook.ipynb'), 'w') as f:
            f.write('{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}')

    def tearDown(self):
        # Clean up the test directory after tests
        for filename in os.listdir(self.test_directory):
            file_path = os.path.join(self.test_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.test_directory)

    def test_conversion(self):
        convert_notebooks_to_python(self.test_directory)
        # Check if the Python file was created
        python_file_path = os.path.join(self.test_directory, 'sample_notebook.py')
        self.assertTrue(os.path.isfile(python_file_path))

    def test_empty_directory(self):
        empty_directory = 'empty_test_directory'
        os.makedirs(empty_directory, exist_ok=True)
        convert_notebooks_to_python(empty_directory)
        # Ensure no files are created in an empty directory
        self.assertEqual(len(os.listdir(empty_directory)), 0)
        os.rmdir(empty_directory)

if __name__ == '__main__':
    unittest.main()
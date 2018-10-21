import unittest
from stringutils import word_wrap_text

# ==============================================================================
class TestStringChallenge(unittest.TestCase):
    '''Performs the unity tests for the first challenge: strings.'''

    # --------------------------------------------------------------------------
    def setUp(self):
        '''Sets up the tests by creating the attributes with the input and the
        expected output strings for the two parts of sample test.'''

        with open('input.txt', mode='r', encoding='utf-8') as file:
            self.input = file.read()

        with open('output_parte1.txt', mode='r', encoding='utf-8') as file:
            self.output_part1 = file.read()

        with open('output-parte2.txt', mode='r', encoding='utf-8') as file:
            self.output_part2 = file.read()

    # --------------------------------------------------------------------------
    def test_empty_string(self):        
        '''Tests that empty strings are unchanged.'''

        output = word_wrap_text('')
        self.assertEqual(output, '')

    # --------------------------------------------------------------------------
    def test_input_sample_part1(self):
        '''Tests that the part 1 of the sample test performs correctly.'''

        output = word_wrap_text(self.input)
        self.assertEqual(output, self.output_part1)

    # --------------------------------------------------------------------------
    def test_input_sample_part2(self):
        '''Tests that the part 2 of the sample test performs correctly.'''

        output = word_wrap_text(self.input, justify=True)
        self.assertEqual(output, self.output_part2)

# ==============================================================================
if __name__ == '__main__':
    unittest.main()
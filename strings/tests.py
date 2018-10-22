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

        with open('lorem_input.txt', mode='r', encoding='utf-8') as file:
            self.lorem = file.read()

        with open('lorem_output1.txt', mode='r', encoding='utf-8') as file:
            self.lorem_output1 = file.read()

        with open('lorem_output2.txt', mode='r', encoding='utf-8') as file:
            self.lorem_output2 = file.read()

        with open('lorem_output3.txt', mode='r', encoding='utf-8') as file:
            self.lorem_output3 = file.read()

    # --------------------------------------------------------------------------
    def test_empty_string(self):        
        '''Tests that empty strings are unchanged.'''

        output = word_wrap_text('')
        self.assertEqual(output, '')

    # --------------------------------------------------------------------------
    def test_many_calls(self):
        '''Tests that the code work for any max line length between 0 and 100.'''
        n = 100
        for i in range(n):
            with self.subTest(i):
                output = word_wrap_text(self.input, max_line_len=i, justify=False)
                self.assertGreater(len(output), 0)
            with self.subTest(n + i):
                output = word_wrap_text(self.input, max_line_len=i, justify=False)
                self.assertGreater(len(output), 0)

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

    # --------------------------------------------------------------------------
    def test_lorem_sample_part1(self):
        '''Tests that the part 1 of the lorem-ipsum sample performs correctly.'''

        output = word_wrap_text(self.lorem, max_line_len=80, justify=False)
        self.assertEqual(output, self.lorem_output1)

    # --------------------------------------------------------------------------
    def test_lorem_sample_part2(self):
        '''Tests that the part 2 of the lorem-ipsum sample performs correctly.'''

        output = word_wrap_text(self.lorem, max_line_len=80, justify=True)
        self.assertEqual(output, self.lorem_output2)

    # --------------------------------------------------------------------------
    def test_lorem_sample_part3(self):
        '''Tests that the part 3 of the lorem-ipsum sample performs correctly.
        That means, test if using values of max line length equal to 0 or 1
        will always break the text to have one word per line.
        '''

        for i in range(2):
            with self.subTest(i):
                output = word_wrap_text(self.lorem, max_line_len=i, justify=False)
                self.assertEqual(output, self.lorem_output3)
            with self.subTest(2+i):
                output = word_wrap_text(self.lorem, max_line_len=i, justify=True)
                self.assertEqual(output, self.lorem_output3)

# ==============================================================================
if __name__ == '__main__':
    unittest.main()
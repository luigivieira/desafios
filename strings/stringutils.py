import re

# ------------------------------------------------------------------------------
def _build_unjustified_paragraph(words, max_line_len):
    '''Builds an unjustified paragraph from the given list of words considering
    the given maximum line length.

    Parameters
    ----------
        words (list). List of strings with the words to be used to build the
        paragraph. The order in the list will be the order of the words in the
        paragraph.

        max_line_length (int). The maximum length of each line in the paragraph.
        If a word can not be added to the current line without exceeding this
        limit, it will be added at the start of a next line.

    Returns
    -------
        paragraph (str). The string with all words added in \n separated lines
        to form a paragraph where each line has at most max_line_len columns.
    '''
    lines = []
    line = ''
    for word in words:
        added = (' ' if len(line) > 0 else '') + word
        if len(line + added) <= max_line_len:
            line += added
        else:
            lines.append(line)
            line = word

    if len(line) > 0:
        lines.append(line)

    return '\n'.join(lines)

# ------------------------------------------------------------------------------
def _build_justified_paragraph(words, max_line_len):
    '''Builds a justified paragraph from the given list of words considering
    the given maximum line length. The words are first arranged in order to make
    the paragraph as beautifully arranged as possible (i.e. with lines of
    roughly the same length), and then extra spaces are added in between the
    words to make all lines the exact same length.

    Parameters
    ----------
        words (list). List of strings with the words to be used to build the
        paragraph. The order in the list will be the order of the words in the
        paragraph.

        max_line_length (int). The maximum length of each line in the paragraph.        

    Returns
    -------
        paragraph (str). The string with all words added in \n separated lines
        to form a paragraph where each line has exactly max_line_len columns.
    '''
    return ''

# ------------------------------------------------------------------------------
def word_wrap_text(text, max_line_len=40, justify=False):
    '''Wraps the given text avoiding breaking words and considering the given
    maximum length of lines and the justification option.

    Parameters
    ----------
        text (str). The text to be wrapped.

        max_line_len (int). The max line length (i.e. max number of columns) to
        be considered when wrapping the text. The default is 40.

        justify (bool). An indication if the text should be justified (True) or
        not (False). When set up the justification is achieved by adding enough
        spaces in between the words to guarantee that the all lines have the
        same length after wrapping.

    Returns
    -------
        wrapped_text (str). The text wrapped according to the parameters.
    '''
    paragraphs = text.split('\n')    
    for index, paragraph in enumerate(paragraphs):
        if paragraph != '':
            words = re.split(r'[(\s+)(\n+)]', paragraph)
            if justify:
                paragraphs[index] = _build_justified_paragraph(words, max_line_len)
            else:
                paragraphs[index] = _build_unjustified_paragraph(words, max_line_len)
                
    return '\n'.join(paragraphs)
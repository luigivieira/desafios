import re
import math

# ------------------------------------------------------------------------------
def _break_by_max_len(words, max_line_len):
    '''Breaks the given list of words into a list of lists, so the words are
    separated in lines of the given maximum length.

    Parameters
    ----------
        words (list). A list of words to separate in lists, one for each line.

        max_line_len (int). The maximum length (i.e. number of columns) for each
        line, considering the sum of the length of the words and the single
        space that would be required to separate each word.

    Returns
    -------
        lines (list). A list of lists with a list of words for each line.
    '''
    lines = []
    line = []

    # Simply iterate through the words and calculate their summed length to
    # separate them into different lines with the given maximum length
    for word in words:
        new_line = line + [word]
        line_len = sum(len(word) for word in new_line) + len(new_line) - 1

        if line_len <= max_line_len:
            line = new_line
        else:
            if len(line) > 0:
                lines.append(line)
            line = [word]

    if len(line) > 0:
        lines.append(line)

    return lines

# ------------------------------------------------------------------------------
def _add_justification_spaces(line, req_line_len):
    '''Add spaces to the words in the given list so they will produce a line
    with the exact line length required.

    P.S.: This method adds extra needed spaces to the words in the line so it
    will produce a line with the exact required length when joined by a single
    space. That means that this function *does not* add the single spaces that
    will be required to join the list of words later on.

    Parameters
    ----------
        line (list). A list of words of a single line, to have spaces added
        so the formed line length will be equal to the `req_line_len`.

        req_line_len (int). The required line length for the line to be
        justified.

    Returns
    -------
        justified_line (list). A list of words with extra spaces added to their
        end, so when they are joined with the regular separated spaces the whole
        line will be justified to the length given by `req_line_len`.
    '''
    # Handle the special cases
    if len(line) == 0:
        return line        
    if len(line) == 1:
        line_len = len(line[0])
        needed_spaces = req_line_len - line_len
        line[0] += ' ' * needed_spaces
        return line

    existing_spaces = len(line) - 1
    line_len = sum(len(word) for word in line) + existing_spaces
    needed_spaces = req_line_len - line_len
    step = abs(existing_spaces - needed_spaces)
    if step <= 0 or step >= len(line):
        step = 1

    # Process each word starting from the first one (index 0),
    # jumping in the calculated step (i.e. the absolute difference between
    # the number of needed and existing spaces in the line)    
    word_idx = 0
    while needed_spaces > 0:

        # If the current word is not the last word in the line,
        # then add one of the needed spaces to its end
        if word_idx != len(line) - 1:
            line[word_idx] += ' '
            needed_spaces -= 1

        # If the current word is the last word in the line, then add one of the
        # needed spaces to its begining *only* if there is just one more space
        # to conclude
        elif needed_spaces == 1:
            line[word_idx] = ' ' + line[word_idx]
            needed_spaces -= 1

        # Jump to the next word (circulating the array)
        word_idx += step
        if word_idx >= len(line):                        
            word_idx -= len(line)

            # After one complete passing in the array, decrease the step if
            # it will make the exact same "path" over the words in the next
            # passing (i.e. if the step is a multiple of the number of words)
            if step > 1 and len(line) % step == 0:
                step -= 1

    return line
    
# ------------------------------------------------------------------------------
def word_wrap_text(text, max_line_len=40, justify=False):
    '''Wraps the given text so each line the maximum length. Also justify the
    lines if required.

    Parameters
    ----------
        text (str). The text to be wrapped.

        max_line_len (int). The max line length (i.e. max number of columns for
        each line) to be considered when wrapping the text. The default is 40.

        justify (bool). An indication if the text should be justified (True) or
        not (False). When set up the justification is achieved by adding enough
        spaces in between the words to guarantee that the all lines have the
        same length after wrapping.

    Returns
    -------
        wrapped_text (str). The text wrapped according to the parameters.
    '''
    # Breaks the text into lines, considering each one a paragraph to be 
    # processed individually
    paragraphs = text.split('\n')
    for index, paragraph in enumerate(paragraphs):
        # Ignore empty lines
        if paragraph == '':
            continue

        # Break the current paragraph into words, ignoring any number of spaces
        words = re.split(r'[(\s+)(\n+)]', paragraph)

        # Break the words into lines within the limit of max line length given
        lines = _break_by_max_len(words, max_line_len)

        # If justification is needed, update the lines to add extra spaces
        # to their words so their length - when joined together with a single
        # space - will be exact the value given `max_line_len`
        if justify:
            for idx, line in enumerate(lines):
                lines[idx] = _add_justification_spaces(line, max_line_len)
                
        # Build back the text for the paragraph by joining each word with a 
        # single space character and each line with a line feed character
        paragraphs[index] = '\n'.join([' '.join(line) for line in lines])
                
    # Build back the final text by joining each paragraph with a new line feed
    # character
    return '\n'.join(paragraphs)
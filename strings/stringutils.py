def word_wrap(text, margin=40, justify=False):
    '''Wraps the given text avoiding breaking words and considering the given
    margin.

    Parameters
    ----------
        text (str). The text to be wrapped.

        margin (int). The margin (i.e. max number of columns) to be applied
        when wrapping the text. The default is 40.

        justify (bool). An indication if the text should be justified (True) or
        not (False). When set up the justification is achieved by adding enough
        spaces in between the words to guarantee that the all lines have the
        same length after wrapping.

    Returns
    -------
        wrapped_text (str). The text wrapped according to the parameters.
    '''
    # TBD
    return text
import re


def dasherize(word):
    """Replace underscores with dashes in the string.
    Example::
        >>> dasherize("FooBar")
        "foo-bar"
    Args:
        word (str): input word
    Returns:
        input word with underscores replaced by dashes
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', word)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1)
    return s2.replace('_','-').lower().replace(' ','')

def camel_classify(word):
    """Creating class name based on a word that have a dash or underscore.

        Example::
            >>> classify("foo_bar")
            >>> classify("foo-bar")
            "FooBar"
        Args:
            word (str): input word
        Returns:
            Class name based on input word
        """
    return word.replace('_', ' ').replace('-', ' ').title().replace(' ','')

def camel_function_style(word):
    """Creating class name based on a word that have a dash or underscore.

            Example::
                >>> classify("foo_bar")
                >>> classify("foo-bar")
                "fooBar"
            Args:
                word (str): input word
            Returns:
                Funcation or var name styling based on input word
            """
    classy_name = camel_classify(word)
    first_lowercase_letter = classy_name[:1].lower()
    rest_of_word = classy_name[1:]
    return first_lowercase_letter + rest_of_word

def creating_title_sentence_from_dasherize_word(word):
    return word.replace('-',' ').title()

#Specially used for ABS Microservice Framework naming convention
def change_slash_and_dot_into_dash(word):
    return word.replace('/','-').replace('.','-')


def change_slash_and_dot(word, replaced_string):
    return word.replace('/', replaced_string).replace('.', replaced_string)


def remove_slash_and_dot(word):
    return word.replace('/', '').replace('.', '')

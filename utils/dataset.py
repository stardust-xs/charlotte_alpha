"""
The dataset module: Provides functions that can be used for manipulating
training data.

These functions help to perform tasks that enables the user to cleanup,
fix or modify the training data.

At a glance, the structure of the module is following:
 - sort_lines():        Sorts the lines in the file and saves it. This
                        function is used to debug any redundancies in
                        NLU data.
 - randomize_lines():   Randomizes the lines in the file. This function
                        is used to make the dataset slightly random.
 - replace_data():      Randomly replaces the given words in the file
                        with required word and saves it. It is
                        recommended to use this to replace the common
                        words OR patterns in your dataset.
 - delete_lines():      Randomly deletes lines from the file and saves
                        it. It is recommended to use this function for
                        shrinking the dataset.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - First code.

from typing import List, NoReturn, Text

from charlotte.utils.constants import ENCODING


def sort_lines(file: Text) -> NoReturn:
    """Sorts lines in file.

    file: File whose data needs to be sorted.

    Sorts the lines in the file and saves it. This function is used to
    debug any redundancies in the NLU data.
    """
    with open(file, encoding=ENCODING) as src_file:
        new_list = sorted(set(src_file.readlines()))
    with open(file, 'w', encoding=ENCODING) as src_file:
        for line in new_list:
            src_file.write(line)


def randomize_lines(file: Text) -> NoReturn:
    """Randomizes lines.

    file: File whose lines need to be randomized.

    Randomizes the lines in the file. This function is used to make the
    dataset slightly random.
    """
    from random import shuffle

    with open(file, encoding=ENCODING) as src_file:
        new_list = list(set(src_file.readlines()))
        shuffle(new_list)
        src_file.close()
    with open(file, 'w', encoding=ENCODING) as src_file:
        for line in new_list:
            src_file.write(line)


def replace_data(file: Text,
                 find_words: List,
                 replace_words: List) -> NoReturn:
    """Replaces words or phrases.

    file:          File from which the words needs to be replaced.
    find_words:    List of words to be replaced from the opened file.
    replace_words: List of words to be replaced with in the opened file.

    Randomly replaces the given words in the file with required word and
    saves it.

    Note: It is recommended to use this to replace the common words OR
    patterns in your dataset.
    """
    from random import choice

    with open(file, encoding=ENCODING) as src_file:
        lines = src_file.readlines()
    with open(file, 'w', encoding=ENCODING) as src_file:
        for line in lines:
            if any(word in lines[line] for word in find_words):
                replaced_line = lines[line].replace(choice(find_words),
                                                    choice(replace_words))
                src_file.write(replaced_line)
            else:
                src_file.write(lines[line])


def delete_lines(file: Text, lines_to_retain: int = 1000) -> NoReturn:
    """Deletes lines randomly.

    file:            File from which the lines are to be deleted.
    lines_to_retain: Number of lines to keep in the file.
                     Default: 1000

    Randomly deletes lines from the file and saves it.

    Note: It is recommended to use this function for shrinking the
    dataset.
    """
    from random import choices, shuffle

    with open(file, encoding=ENCODING) as src_file:
        new_list = list(set(src_file.readlines()))
        shuffle(new_list)
    with open(file, 'w', encoding=ENCODING) as src_file:
        if int(lines_to_retain) is None:
            shrunked_list = choices(new_list, k=1000)
        else:
            shrunked_list = choices(new_list, k=int(lines_to_retain))
        for line in shrunked_list:
            src_file.write(line)

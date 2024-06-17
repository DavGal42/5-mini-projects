"""
Author: David Galstyan

Description: This is a script that checks the orthographic mistakes in the given text.
It finds the mistakes and tries to correct them with the help of the user.
It should suggest versions for the correct word, and the user should choose the best one.
The script takes 2 arguments: “-input” for the input file, “-output” for the output file.
"""

import argparse
from spellchecker import SpellChecker


spell = SpellChecker()


def get_fnames():
    """
        Use argparse to get names of the input and output files
        Returns: input and output files names
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-input', help='Input file name')
    parser.add_argument('-output', help='Output file name')

    args = parser.parse_args()

    return args.input, args.output


def get_content(fname):
    """
        Open the file and read it
        Parameters: name of the file
        Returns: content of the file
    """
    with open(fname, 'r', encoding='utf-8') as f:
        return f.read()


def get_words(cnt):
    """
        Get each word in the file in a list
        Parameters: content of the file
        Returns: each word of the file
    """
    words = cnt.split()
    return words


def check_words(words):
    """
        Correct the wrong words and replace them
        Parameters: each word of the file
        Returns: corrected words
    """
    for i, v in enumerate(words):
        
        if v not in spell:
            correct = list(spell.candidates(v))
            print(f'Wrong word: {words[i]}')
            print('The word is not correct. Choose from these:')
            print(correct)
            choose = input('Choose: ')
            words[i] = choose
    return words


def write_in_file(fname, correct_str):
    """
        Open the file, join the list of words, and put them into the file
        Parameters: filename and correct words
        Returns: file with corrected text
    """
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(' '.join(correct_str))


def main():
    """
        The main function
    """
    input_file, output_file = get_fnames()
    cnt = get_content(input_file)
    words = get_words(cnt)
    correct_txt = check_words(words)
    write_in_file(output_file, correct_txt)
    new_cnt = get_content(output_file)
    print(new_cnt)


if __name__ == "__main__":
    main()

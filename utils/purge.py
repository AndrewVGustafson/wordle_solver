"""Deals with parsing, sorting, and manipulating given wordle data."""
from typing import Any

def purge_wrong(letters: list, words: list) -> list:
    """
    Returns a purged version of inputted list, without any words containing `letters`.

    Args:
        letters (list): Characters that are not included in any part of the correct word
        words (list): Current list of words

    Returns:
        list: List of words without `letters`
    """
    letters = list(set(letters))
    purged_words = words
    for letter in letters:
        purged_words = [word for word in purged_words if letter not in word]
    return purged_words

def purge_wrong_location(blocks: dict, words: list) -> list:
    purged_words = words
    for letter, position in blocks:
        purged_words = [
            word for word in purged_words
            if letter in word and letter not in word[position]
            ]
    return purged_words

def purge_correct(blocks: dict, words: list) -> list:
    purged_words = words
    for letter, position in blocks:
        purged_words = [
            word for word in purged_words
            if letter in word and letter in word[position]
            ]
    return purged_words

def filter_words(tiles_data: dict[str, Any], words: list) -> list:
    purged_words = words
    for data_state, values in tiles_data.items():
        if data_state == "wrong":
            purged_words = purge_wrong(values, purged_words)

        if data_state == "wrong-location":
            purged_words = purge_wrong_location(values, purged_words)

        if data_state == "correct":
            purged_words = purge_correct(values, purged_words)

    return purged_words

def better_guess(words: list) -> str:
    better_words = []
    for word in words:
        if len(list(set(word))) == 5:
            better_words.append(word)

    if better_words:
        return better_words[0]

    return words[0]

def better_guesses(words: list) -> list:
    better_words = []
    for word in words:
        if len(list(set(word))) == 5:
            better_words.append(word)

    if better_words:
        return better_words

    return words


def get_starting_words(starting_words: list) -> list:
    while len(starting_words) < 6:
        starting_words.append(None)
    return starting_words

def blocks_to_list(blocks: str) -> list[tuple[str, int]]:
    try:
        return [(block[0], int(block[1]) - 1) for block in blocks]
    except FileExistsError:
        pass

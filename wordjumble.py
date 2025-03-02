#!python3

import itertools
import time

def get_file_lines(filename='/usr/share/dict/words'):
    with open(filename) as file:
        lines = [line.strip().upper() for line in file]
    return lines

def sorted_letters(scrambled_letters):
    return ''.join(sorted(scrambled_letters))

def sorted_dictionary(words_list):
    sorted_dict = {}
    for word in words_list:
        sorted_word = sorted_letters(word)
        if sorted_word in sorted_dict:
            sorted_dict[sorted_word].append(word)
        else:
            sorted_dict[sorted_word] = [word]
    return sorted_dict

def solve_one_jumble(letters):
    target_letters = sorted_letters(letters)
    for sorted_dictionary_key in sorted_dict:
        if len(sorted_dictionary_key) == len(target_letters):
            if sorted_dictionary_key == target_letters:
                return sorted_dict[sorted_dictionary_key]
    return []

def solve_final_jumble(letters, final_circles):
    num_circles = sum(len(circles) for circles in final_circles)
    if num_circles != len(letters):
        print('Number of circles does not match number of letters.')
        return []
    if len(final_circles) == 1:
        words = solve_one_jumble(letters)
        return [(word,) for word in words]

    valid_phrases = []
    group_sizes = [len(circle) for circle in final_circles]

    def find_valid_phrases(remaining_letters, current_phrase, remaining_group_sizes):
        if not remaining_group_sizes:
            valid_phrases.append(tuple(current_phrase))
            return

        current_length = remaining_group_sizes[0]

        for combination in itertools.combinations(remaining_letters, current_length):
            valid_words = solve_one_jumble(combination)

            if valid_words:
                new_remaining = list(remaining_letters)
                for letter in combination:
                    new_remaining.remove(letter)
                new_remaining = ''.join(new_remaining)

                for word in valid_words:
                    find_valid_phrases(new_remaining, current_phrase + [word], remaining_group_sizes[1:])

    find_valid_phrases(letters, [], group_sizes)
    return sorted(set(valid_phrases))

def solve_word_jumble(letters, circles, final):
    final_letters = ''

    for index in range(len(letters)):
        scrambled_letters = letters[index]
        circled_blanks = circles[index]
        words = solve_one_jumble(scrambled_letters)
        print(f'Jumble {index+1}: {scrambled_letters} => ', end='')
        if len(words) == 0:
            print('(no solution)')
            continue
        print(f'unscrambled into {len(words)} words: {" or ".join(words)}')

        for letter, blank in zip(words[0], circled_blanks):
            if blank == 'O':
                final_letters += letter

    if len(final_letters) == 0:
        print('Did not solve any jumbles, so could not solve final jumble.')
        return

    final_results = solve_final_jumble(final_letters, final)

    print(f'Final Jumble: {final_letters} => ', end='')
    if len(final_results) == 0:
        print('(no solution)')
        return
    print(f'unscrambled into {len(final_results)} possible phrases:')
    for num, result in enumerate(final_results):
        print(f'    Option {num+1}: {" ".join(result)}')


def test_solve_word_jumble_1():
    print('='*20 + ' WORD JUMBLE TEST CASE 1 ' + '='*20)
    # Cartoon prompt for final jumble:
    # "What her ears felt like at the rock concert: _______."
    letters = ['ACOME', 'FEROC', 'REDDEG', 'YURFIP']
    circles = ['___O_', '__OO_', 'O_O___', 'O__O__']
    final = ['OOOOOOO']  # Final jumble is 1 word with 7 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_2():
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 2 ' + '='*20)
    # Cartoon prompt for final jumble:
    # "What a dog house is: ____ ___."
    letters = ['TARFD', 'JOBUM', 'TENJUK', 'LETHEM']
    circles = ['____O', '_OO__', '_O___O', 'O____O']
    final = ['OOOO', 'OOO']  # Final jumble is 2 words with 4 and 3 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_3():
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 3 ' + '='*20)
    # Cartoon prompt for final jumble:
    # "A bad way for a lawyer to learn the justice system: _____ and _____."
    letters = ['LAISA', 'LAURR', 'BUREEK', 'PROUOT']
    circles = ['_OOO_', 'O_O__', 'OO____', '__O_OO']
    final = ['OOOOO', 'OOOOO']  # Final jumble is 2 words with 5 and 5 letters
    solve_word_jumble(letters, circles, final)


def test_solve_word_jumble_4():
    print('\n' + '='*20 + ' WORD JUMBLE TEST CASE 4 ' + '='*20)
    # Cartoon prompt for final jumble:
    # "Farley rolled on the barn floor because of his __-______."
    letters = ['TEFON', 'SOKIK', 'NIUMEM', 'SICONU']
    circles = ['__O_O', 'OO_O_', '____O_', '___OO_']
    final = ['OO', 'OOOOOO']  # Final jumble is 2 words with 2 and 6 letters
    solve_word_jumble(letters, circles, final)


if __name__ == '__main__':
    words_list = get_file_lines('/usr/share/dict/words')

    sorted_dict = sorted_dictionary(words_list)
    start_time = time.time()
    test_solve_word_jumble_1()
    test_solve_word_jumble_2()
    test_solve_word_jumble_3()
    test_solve_word_jumble_4()
    print ('Elapsed time: {:.2f} seconds'.format(time.time() - start_time))

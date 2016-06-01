#
# markov.py - 2016-06-01 Steven Wart created this file
#
# Generate a string of characters conforming to first, second and third-order statistical distributions of English text
#
# Statistical distributions from http://www.data-compression.com/english.html
#
from __future__ import print_function
from random import random

alphabet = [chr(code) for code in range(ord('a'),ord('z')+1)]
# S represents a break between words
alphabet.append('S')

def read_stats(filename, read_prefix=False):
    results = {}
    with open(filename) as stats_file:
        for line in stats_file:
            index = 0
            stats = line.split()
            if read_prefix:
                prefix = stats[0]
                for stat in stats[1:]:
                    results[prefix + alphabet[index]] = float(stat)
                    index = index + 1
            else:
                for stat in stats:
                    results[alphabet[index]] = float(stat)
                    index = index + 1
    return results

first_order_stats = read_stats('stat1_out.txt')
second_order_stats = read_stats('stat2_out.txt', True)
third_order_stats = read_stats('stat3_out.txt', True)

# total = sum([val for val in first_order_stats.values()])
# print("first order stats:", first_order_stats)
# print("first order stats total %3.1f" % total)

cumulative1 = []
cumulative_sum = 0.0
for ch in alphabet:
    cumulative_sum = cumulative_sum + first_order_stats[ch]
    cumulative1.append([cumulative_sum, ch])

# print("cumulative totals for first order stats:", cumulative1)

# print("second order stats totals:")
# for ch1 in alphabet:
#     total = sum([second_order_stats[ch1+ch2] for ch2 in alphabet])
#     print("%s: %3.1f" % (ch1, total), end=", ")
# print()

cumulative2 = {}
for ch1 in alphabet:
    cumulative2[ch1] = []
    cumulative_sum = 0.0
    for ch2 in alphabet:
        cumulative_sum = cumulative_sum + second_order_stats[ch1+ch2]
        cumulative2[ch1].append([cumulative_sum, ch1+ch2])

# print("cumulative totals for second order stats:", cumulative2)

# print("third order stats totals:")
# for ch1 in alphabet:
#     for ch2 in alphabet:
#         total = sum([third_order_stats[ch1+ch2+ch3] for ch3 in alphabet])
#         print("%s: %3.1f" % (ch1+ch2, total), end=", ")
# print()

cumulative3 = {}
for ch1 in alphabet:
    for ch2 in alphabet:
        cumulative3[ch1+ch2] = []
        cumulative_sum = 0.0
        for ch3 in alphabet:
            cumulative_sum = cumulative_sum + third_order_stats[ch1+ch2+ch3]
            cumulative3[ch1+ch2].append([cumulative_sum, ch3])

# print("cumulative totals for third order stats:", cumulative3)

def lookup_char(prev1, prev2):
    # print("lookup_char: prev1=%s, prev2=%s" % (prev1, prev2))
    lookup = random()
    if len(prev1) == 0:
        cumulative_totals = cumulative1
    elif len(prev2) == 0:
        cumulative_totals = cumulative2[prev1]
    else:
        cumulative_totals = cumulative3[prev2]

    for pair in cumulative_totals:
        if lookup <= pair[0]:
            return pair[1]

    # should not happen if the statistics are properly defined
    return None

prev1 = ''
prev2 = ''
letter_count = 0
word_count = 0
for i in range(1000):
    ch = lookup_char(prev1, prev2)
    if len(ch) == 2:
        prev1 = ch[0]
        ch = ch[1]
    if len(prev1) > 0:
        prev2 = prev1 + ch
    prev1 = ch
    if len(ch) == 0:
        continue
    # if letter_count > 0 and letter_count % 5 == 0:
    #     word_count = word_count + 1
    #     print(' ', end='')
    #     if word_count % 15 == 0:
    #         print('')
    print(ch.replace('S', ' '), end='')
    letter_count = letter_count + 1
print()
# /usr/bin/env python
# -*- coding: utf-8 -*-
# author: baiyinchuan

import argparse
import codecs
import os

from collections import Counter


def count_surname_in_poets(poets_file_path, all_surnames_file_path, poet_surname_file_path):
    surname_count = Counter()
    surname_poet_dict = dict()
    with codecs.open(poets_file_path, 'r', 'utf8') as poets_file, \
            codecs.open(all_surnames_file_path, 'r', 'utf8') as surnames_file, \
            codecs.open(poet_surname_file_path, 'w', 'utf8') as poet_surname_file:
        surnames_set = set()
        for line in surnames_file:
            surnames_set.add(line.strip())

        for line in poets_file:
            poet = line.strip()

            poet_name_length = len(poet)
            poet_surname = ''
            for i in range(poet_name_length):
                poet_surname = poet[:poet_name_length-i-1]
                if poet_surname in surnames_set:
                    surname_count[poet_surname] += 1
                    surname_poet_set = surname_poet_dict.setdefault(poet_surname, set())
                    surname_poet_set.add(poet)
                    break
            poet_surname_file.write('\t'.join([poet, poet_surname])+'\n')

    return surname_count, surname_poet_dict


def stat_poet_surname(surname_count, surname_poet_dict):
    def print_counter(counter):
        for k, v in counter:
            print(k, v)

    # 诗人姓氏数量排名
    print('\n诗人中姓氏数量排名')
    print_counter(surname_count.most_common(10))
    print('\n')

    for c in ['白', '马']:
        print(c, surname_count[c])
        print(surname_poet_dict[c])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poets_file_path', type=str, default='../data/poets.txt',
                        help='file path of poets')
    parser.add_argument('--all_surnames_file_path', type=str, default='../data/all_surnames.txt',
                        help='file path to all surnames')
    parser.add_argument('--poet_surname_file_path', type=str, default='../data/poet_sruname.txt',
                        help='file path to save surname of poet')
    args = parser.parse_args()

    surname_count, surname_poet_dict = count_surname_in_poets(args.poets_file_path, args.all_surnames_file_path, args.poet_surname_file_path)
    stat_poet_surname(surname_count, surname_poet_dict)


if __name__ == '__main__':
    main()

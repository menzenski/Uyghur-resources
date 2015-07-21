#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## ipatranscriber.py Version 1.0 (2015-07-21)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: MIT ( http://opensource.org/licenses/MIT )
##
##
### The MIT License (MIT)
###
### Copyright (c) 2015 Matt Menzenski
###
### Permission is hereby granted, free of charge, to any person obtaining a
### copy of this software and associated documentation files (the "Software"),
### to deal in the Software without restriction, including without limitation
### the rights to use, copy, modify, merge, publish, distribute, sublicense,
### and/or sell copies of the Software, and to permit persons to whom the
### Software is furnished to do so, subject to the following conditions:
###
### The above copyright notice and this permission notice shall be included in
### all copies or substantial portions of the Software.
###
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
### OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
### THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
### FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
### DEALINGS IN THE SOFTWARE.
##
##########

"""
Take a list of Uyghur words and add broad IPA transcription.

The input:

    yéziliq
    zeple-
    yashliq
    a'ile

Returns the output:

    yéziliq;jeziliqʰ
    zeple-;zɛplɛ-
    yashliq;jaʃliqʰ
    a'ile;aˀilɛ

The IPA output is largely a one-to-one substitution of graphs or digraphs for
their phonemic values, with the exception that aspiration is blocked consonants.
"""

from __future__ import unicode_literals
import codecs

## our Uyghur word list
input_file = "uyghuritems.txt"

## orthography/IPA pairs in which one or both members are digraphs
uyghur_multiples = {
    "ch": "ʧʰ",
    "gh": "ɣ",
    "ng": "ŋ",
    "sh": "ʃ",
    "zh": "ʒ",
    "p": "pʰ",
    "t": "tʰ",
    "q": "qʰ",
    "k": "kʰ",
    ",": " | ",
    ".": " | ",
    ":": " | ",
    ";": " | ",
    "?": " | ",
    "!": " | "
    }

## orthography/IPA pairs in which both members are a single character
## (pairs in which IPA and orthography are equal don't need to be replaced.)
uyghur_singles = {
    "e": "ɛ",
    "é": "e",
    "x": "χ",
    "j": "ʤ",
    "ö": "ø",
    "‘": "ˀ",
    "'": "ˀ"
    }

## y and j get treated separately, since both symbols are input of one process
## and output of another (i.e., otherwise, we'd get ʤ as output when we want j)
uyghur_y = {
    "y": "j"
    }

uyghur_u = {
    "ü": "y"
    }

def uyghur_latin_to_ipa(word):
    """Return broad IPA transcription of a Uyghur word in Latin orthography."""

    ## new_word will be the output. start by setting it equal to the input
    new_word = word

    ## first replace the diagraphs
    for char in uyghur_multiples.keys():
        new_word = new_word.replace(char, uyghur_multiples[char])

    ## then the single characters
    for char in uyghur_singles.keys():
        new_word = new_word.replace(char, uyghur_singles[char])

    ## then y
    for char in uyghur_y.keys():
        new_word = new_word.replace(char, uyghur_y[char])

    ## then j
    for char in uyghur_u.keys():
        new_word = new_word.replace(char, uyghur_u[char])

    ## list of Uyghur consonants (from "uigCLpixzd2ipa.xsl")
    consonants = [
        "b", "d", "g", "ɣ", "h", "χ", "ʤ", "k", "q", "l", "ɫ", "m", "n",
        "ŋ", "p", "r", "s", "ʃ", "t", "ʧ", "w", "j", "z", "ʒ"
        ]

    ## create a list of aspiration ("ʰ") + consonant sequences
    sequences = ["ʰ" + consonant for consonant in consonants]

    ## replace sequences of ʰ + consonant with the plain consonant
    for sequence in sequences:
        new_word = new_word.replace(sequence, sequence[1:])

    ## output the word in IPA transcription
    return new_word

def main():
    ## open input file in read-only mode with utf-8 encoding
    with codecs.open(input_file, mode='r', encoding='utf-8') as words:
        for line in words:
            ## replace spaces with an underscore---we'll undo this later
            ## (lines get split on whitespace, so this keeps entries together)
            line = line.replace(" ", "_")
            for word in line.split():
                myipa = uyghur_latin_to_ipa(word)
                ## output with a semicolon between for straightforward
                ## pasting into a spreadsheet
                print "{};{}".format(
                    word.replace("_"," "), myipa.replace("_", " "))

## run the main() function if this script is called as a standalone script
## (but if imported, e.g., using the call
## from adduyghuripa import uyughur_latin_to_ipa
## the main() function won't run)
if __name__ == "__main__":
    main()

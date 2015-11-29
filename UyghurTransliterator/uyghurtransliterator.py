#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## uyghurtransliterator.py Version 0.2 (2015-11-09)
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

"""Convert a Uyghur text between different orthographies."""

from __future__ import print_function

import codecs
import sys

def to_unicode_or_bust(obj, encoding='utf-8'):
    """Ensure that an object is unicode."""
    # function by Kuman McMillan ( http://farmdev.com/talks/unicode )
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

class UyghurString(object):
    """String object containing text in the Uyghur language."""

    def __init__(self, input_text, input_orth):
        """Initialize text object.

        Parameters
        ---------
          input_text (str): string containing Uyghur text
          input_orth (str): input orthography --- must be one of these:
            'IPA', 'UyArabic', 'UyLatin', 'UyCyrillic', 'ChineseLatin',
            'MengesLatin', 'JarringLatin', 'JarringArabic', 'MalovLatin'
        """
        self.input_text = input_text
        self.input_orth = input_orth
        self.orth_key = {
            'IPA': 0,
            'UyArabic': 1,
            'UyLatin': 2,
            'UyCyrillic': 3,
            'ChineseLatin': 4,
            'MengesLatin': 5,
            'JarringLatin': 6,
            'JarringArabic': 7,
            'MalovLatin': 8
            }
        self.uyghur_orthographies = (
            (u'a', u'\u0627', u'a', u'а', u'a', u'a', u'a', 7, u'а'),
            (u'ɑ', u'\u0627', u'a', u'а', u'a', u'á', u'a', 7, 8),
            (u'aː', u'\u0627', u'a', u'а', u'a', u'ā', u'aː', u'\u0627', 8),
            (u'ɛ', u'\u06D5', u'e', u'е', u'e', u'ä', u'ɛ', u'\u06D5', u'ӓ'),
            (u'æ', u'\u06D5', u'e', u'е', u'e', u'ä', u'æ', u'\u06D5', 8),
            (u'b', u'\u0628', u'b', u'б', u'b', u'b', u'b', u'\u0628', u'б'),
            (u'd', u'\u062F', u'd', u'д', u'd', u'd', u'd', u'\u062F', u'д'),
            (u'e', u'\u06D0', u'ë', u'е', u'e', u'e', u'e', 7, u'е'),
            (u'f', u'\u0641', u'f', u'ф', u'f', u'f', u'f', u'\u0641', 8),
            (u'ɡ', u'\u06AF', u'g', u'г', u'g', u'g', u'g', u'\u06AF', u'г'),
            (u'ɣ', u'\u063A', u'gh', u'ғ', u'ƣ', u'ɣ', u'ɣ', u'\u063A', u'ҕ'),
            (u'h', u'\u0647', u'h', u'һ', u'ħ', u'h', u'h', u'\u0647', 8),
            (u'χ', u'\u062E', u'x', u'х', u'h', u'x', u'χ', u'\u062E', u'х'),
            (u'i', u'\u0649', u'i', u'и', u'i', u'i', u'i', u'\u0649', u'i'),
            (u'ɨ', u'\u0649', u'i', u'и', u'i', u'i', u'ï', u'\u0649', u'ы'),
            (u'dʒ', u'\u062C', u'j', u'ж', u'j', u'dž', u'dʒ', u'\u062C', u'з'),
            (u'kʰ', u'\u0643', u'k', u'k', u'k', u'k', u'k', u'\u0643', u'k'),
            (u'qʰ', u'\u0642', u'q', u'к', u'ḳ', u'q', u'q', u'\u0642', u'к'),
            (u'l', u'\u0644', u'l', u'л', u'l', u'l', u'l', u'\u0644', u'л'),
            (u'ł', u'\u0644', u'l', u'л', u'l', u'ł', u'l', u'\u0644', u'l'),
            (u'm', u'\u0645', u'm', u'м', u'm', u'm', u'm', u'\u0645', u'м'),
            (u'n', u'\u0646', u'n', u'н', u'n', u'n', u'n', u'\u0646', u'н'),
            (u'ŋ', u'\u06AD', u'ng', u'ң', u'ng', u'ñ', u'ŋ', u'\u06AD', u'ң'),
            (u'o', u'\u0648', u'o', u'о', u'o', u'o', u'o', u'\u0648', u'о'),
            (u'ø', u'\u06C6', u'ö', u'ө', u'ɵ', u'ö', u'ö', u'\u0648', u'ӧ'),
            (u'pʰ', u'\u067E', u'p', u'п', u'p', u'p', u'p', u'\u067E', u'п'),
            (u'r', u'\u0631', u'r', u'р', u'r', u'r', u'r', u'\u0631', u'р'),
            (u's', u'\u0633', u's', u'с', u's', u's', u's', u'\u0633', u'с'),
            (u'ʃ', u'\u0634', u'sh', u'ш', u'x', u'š', u'š', u'\u0634', u'ш'),
            (u'tʰ', u'\u062A', u't', u'т', u't', u't', u't', u'\u062A', u'т'),
            (u'tʃʰ', u'\u0686', u'ch', u'ч', u'q', u'č', u'č', u'\u0686', u'ч'),
            (u'u', u'\u06C7', u'u', u'у', u'u', u'u', u'u', u'\u0648', u'у'),
            (u'ɯ', u'\u06C7', u'u', u'у', u'u', u'ŏ', u'ɯ', u'\u0648', 8),
            (u'ʏ', u'\u06C7', u'u', u'у', u'u', u'ů', u'ů', u'\u0648', 8),
            (u'y', u'\u06C8', u'ü', u'ү', u'ü', u'ü', u'ů', u'\u06C8', 8),
            (u'yː', u'\u06C8', u'ü', u'ү', u'ü', u'ṻ', u'ůː', u'\u06C8', u'ӱ'),
            (u'ŭ', u'\u06C7', u'u', u'у', u'u', u'u', u'ŭ', u'\u06C8', 8),
            (u'w', u'\u06CB', u'w', u'в', u'w', u'w', u'v', u'\u06CB', u'в'),
            (u'j', u'\u064A', u'y', u'й', u'y', u'j', u'j', 7, u'ĭ'),
            (u'z', u'\u0632', u'z', u'з', u'z', u'z', u'z', u'\u0632', u'z'),
            (u'ʒ', u'\u0698', u'zh', u'ж', u'zh', u'ž', 6, 7, u'з'),
            (u'ʔ', u'\u0621', u"'", 3, u"'", u"'", u"'", 7, 8),
            (0, u'\u0626', u'', 3, 4, 5, 6, 7, 8),
            (0, u'\u06BE', u'h', 3, 4, 5, 6, 7, 8),
            )

    def as_string(self):
        """Read the input file's contents into a string."""
        with codecs.open(self.input_text, 'r+', encoding='utf-8') as f:
            return to_unicode_or_bust(f.read().replace(u'\n', u''))

    def transliterate(self, output_orth, input_string=None):
        """Transliterate text to specified output orthography.

        Parameters
        ---------
          output_orth (str): output orthography --- must be one of these:
            'IPA', 'UyArabic', 'UyLatin', 'UyCyrillic', 'ChineseLatin',
            'MengesLatin', 'JarringLatin', 'JarringArabic', 'MalovLatin'
        """
        if input_string == None:
            input_string = self.as_string()

        idx_c = self.orth_key[self.input_orth]
        idx_d = self.orth_key[output_orth]

        ## TODO: fix this case handling. This should give correct output for
        ## the three orthographies that don't distinguish case, but it won't
        ## transliterate an upper-case letter to another upper-case letter.
        ## TODO: make an upper-case version of the orthography dict?
        ## e.g., something like:
        ## try:
            ## upper_case = tup[idx_c].upper() ## for every entry?
        caseless_orths = ['IPA', 'UyArabic', 'JarringArabic']
        if output_orth in caseless_orths:
            text_in = input_string.lower()
            text_out = input_string.lower()
        elif output_orth not in caseless_orths:
            text_in = input_string
            text_out = input_string
        ## TODO: Make the above more elegant

        for tup in self.uyghur_orthographies:
            input_char = tup[idx_c]
            output_char = tup[idx_d]

            if isinstance(input_char, int) or isinstance(output_char, int):
                pass
            else:
                text_out = text_out.replace(input_char, output_char)

        return text_out

def main(input_file, input_orth, output_orth, output_file=None):
    """Convert file contents from one orthography to another."""
    if output_file == None:
        output_file = input_file
    uy = UyghurString(input_file, input_orth)
    with codecs.open(output_file, 'w+', encoding='utf-8') as stream:
        stream.write(uy.transliterate(output_orth))

if __name__ == "__main__":
    if len(sys.argv) == 5:
        in_file = sys.argv[1]  # input filename
        in_orth = sys.argv[2]  # input orthography
        out_orth = sys.argv[3] # output orthography
        out_file = sys.argv[4] # output filename

        main(in_file, in_orth, out_orth, out_file)

    elif len(sys.argv) == 4:
        in_file = sys.argv[1]  # input filename
        in_orth = sys.argv[2]  # input orthography
        out_orth = sys.argv[3] # output orthography

        main(in_file, in_orth, out_orth)

    else:
        print("\nUSAGE:\n\tpython uyghurtransliterator.py "
              "inputfilename.txt inputOrthography outputOrthography "
              "(outputfilename.txt)\n\n"
              "inputOrthograpy and outputOrthography must be one of these:\n"
              "\t'IPA', 'UyArabic', 'UyLatin', 'UyCyrillic', 'ChineseLatin'\n"
              "\t'MengesLatin', 'JarringLatin', 'JarringArabic', 'MalovLatin'\n")

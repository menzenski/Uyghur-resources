# Uyghur Transliterator

This script takes as input a list of Uyghur words in Latin orthography (one
word per line) and returns a list of those words and their broad phonemic
transcriptions (one word and its transcription per line).

## Usage

The script may be imported as a module, but was written to be called from the
command line. The template is `python uyghurtransliterator.py inputfilename.txt inputOrthography outputOrthography (outputfilename.txt)`, where `inputfilename.txt` is the name of the input file, `inputOrthography` and
`outputOrthography` are, respectively, the name of the orthography used in the
input file and the desired output orthography, and `outputfilename.txt` is the
name of the output file. The name of the output file is optional: if one is not
supplied, the input file will be overwritten with the results of the
transliteration.

## Supported orthographies

* `IPA` -- the International Phonetic Alphabet
* `UyArabic` -- Uyghur Arabic
* `UyLatin` -- Uyghur Latin
* `UyCyrillic` -- Uyghur Cyrillic
* `ChineseLatin`
* `MengesLatin`
* `JarringLatin`
* `JarringArabic`
* `MalovLatin`

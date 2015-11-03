# Uyghur IPA Transcriber

This script takes as input a list of Uyghur words in Latin orthography (one
word per line) and returns a list of those words and their broad phonemic
transcriptions (one word and its transcription per line).

Thus the input:

```
yéziliq
zeple-
yashliq
a'ile
```

Returns the output:

```
yéziliq;jeziliqʰ
zeple-;zɛplɛ-
yashliq;jaʃliq
a'ile;aˀilɛ
```

The IPA output is largely a one-to-one substitution of graphs or digraphs for
their phonemic values, with the exception that aspiration is blocked before consonants.
Future versions of this script will take other orthographies (i.e., Uyghur
Perso-Arabic script and Uyghur Cyrillic) as input.

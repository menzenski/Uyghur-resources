# Wiktionary Scraper

I have access to a Uyghur lexicon with 33,810 headwords, but only about a fifth
of those entries have a translation provided in English. Most entries are
glossed in Mandarin instead. I don't know Mandarin, and needed a way to get
high-quality English translations of those Mandarin glosses.

To that end, I threw together the script `wiktionaryscraper.py`, which does two
things:

1. Fetches English translations (from [Wiktionary](https://en.wiktionary.org))
of those Mandarin glosses
2. Preserves the original order of the input (both the order of multiple
    Mandarin glosses in one line as well as the order of lines are respected)

Each line of the input file takes the form `[numeral],[Mandarin gloss(es)]`,
with the numeral and comma mandatory and the Mandarin gloss(es) optional. The
following lines are all valid input:

```
4745,小心；轻轻地
4746,响应
4747,
4748,
```

The output is formatted in much the same way, only with a semicolon rather than
a comma separating the numeral and the gloss (for easier copy-pasting into a
spreadsheet). The output corresponding to the above input example looks like
this:

```
4745;careful (小心),
4746;to respond, to answer (响应),
4747;
4748;
```

Note that only the first of the two Mandarin glosses in line 4745 has an entry
on Wiktionary, so only that gloss returns an English translation in the output.
The Mandarin gloss follows its English translation in parentheses.

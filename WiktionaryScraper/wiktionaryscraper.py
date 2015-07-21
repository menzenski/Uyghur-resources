#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## wiktionaryscraper.py Version 1.0 (2015-07-20)
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
Get English translation from Wiktionary of each Mandarin word in a list.

Take as input a text file in which each line contains a numeral and one
or more Mandarin terms, separated by a comma, and return a text file in
which each line contains a numeral (in the same order as in the input
file) followed by a translation of each Mandarin term in that line (if
a Wiktionary page exists for that term).

E.g., the line

    48,生气，发怒

in the input yields

    48;angry (生气), (literary) to become angry (发怒),

in the output.
"""

#from __future__ import unicode_literals
from bs4 import BeautifulSoup as Soup
from urllib import FancyURLopener
import urllib2
import codecs
import time
import random

input_file = "uyghurchineseitemswithindex.txt"

results_file = "wiktionaryoutput.txt"


class MyOpener(FancyURLopener):
    """FancyURLopener object with custom User-Agent field."""

    ## regular Mac Safari browser:
    #version = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
    #           "AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 "
    #           "Safari/600.5.17")

    ## identify this web scraper as such
    ## and link to a page with a description of its purpose:
    version = ("Translation scraper created by Matt Menzenski. "
               "See www.menzenski.com/scraper for more information.")

class RowInTheLexicon(object):
    """One line in the input file.


    Expects a file composed of lines with a numeral followed by
    either nothing or one or more Mandarin terms. The following are
    all valid lines:

    104,提醒；警告
    105,收集
    106,
    107,
    """

    def __init__(self, mandarin_cell):
        """Initialize a new row object."""
        self.mandarin_cell = mandarin_cell
        self.index = 0
        self.whole = ''
        self.searchable = []
        self.all_english = []
        self.english = ''
        self.best_translation = ''


    def get_lexicon_info(self, mandarin_cell):
        # TODO: Change name (reserve 'get' prefix for actual getters)
        """Split row into index (int) and Mandarin glosses (list)."""
        try:
            mysplit = mandarin_cell.split(",", 1)
            self.index = int(mysplit[0])
            self.whole = mysplit[1].replace("\n", "")
        except ValueError:
            pass
        else:
            pass

        #tokens = re.split('[；，（）;, ]', self.whole)
        punct = ["；", "，", "（", "）", ";", ",", "(", ")", '"', "'"]
        stripped = self.whole
        for i in punct:
            stripped = stripped.replace(i, " ")

        tokens = stripped.split(" ")

        self.searchable.append(self.whole)
        self.searchable.append(stripped)
        for token in tokens:
            if token != '':
                self.searchable.append(token)

        #while True:
        for _ in range(1,3):
            if len(self.searchable) >= 2:
                if self.searchable[0] == self.searchable[1]:
                    self.searchable = self.searchable[1:]

class WiktionaryEntry(object):
    """Entry on en.wiktionary.org for a Mandarin term."""

    def __init__(self, mandarin_term):
        """Initialize an object for a Mandarin term."""
        self.mandarin_term = mandarin_term
        self.english = []
        self.english_str = ', '.join(self.english)
        self.english_short = ''
        self.address = "http://en.wiktionary.org/wiki/" + mandarin_term

    def check_page(self):
        """Load the actual wiktionary page for a term if it exists."""
        try:
            #html = urllib.urlopen(self.address).read()
            myopener = MyOpener()
            html = myopener.open(self.address).read()
            soup = Soup(html)

            try:
                box = soup.find(
                    "table",
                    style=("border:1px solid #797979; margin-left: 1px; "
                    "text-align:left; width:76%"))
                links = box.find_all("a")

                if len(links) > 0:
                    self.address = "http://en.wiktionary.org" + links[0].get(
                        "href")
                    if self.address.endswith("#Chinese"):
                        self.address = self.address[:-8]
                else:
                    pass

            except AttributeError:
                pass
            else:
                pass

        except urllib2.HTTPError, e:
            print e.code

        except urllib2.URLError, e:
            print e.code

        else:
            pass

    def get_translation(self):
        """Find the translation of a Mandarin term from Wiktionary."""
        try:
            #html = urllib.urlopen(self.address).read()
            myopener = MyOpener()
            html = myopener.open(self.address).read()
            soup = Soup(html)

            try:
                heading = soup.find(
                    "span", {"class": "mw-headline",
                             "id": ["Chinese", "Mandarin"]})

                definition = heading.find_next("ol")

                new_def = definition.li

                self.english.append(new_def.text.split("\n")[0])
                self.english_short = new_def.text.split(
                    "\n")[0].replace(";", ",")

                if new_def.next_sibling.next_sibling:
                    while True:
                        newer_def = new_def.next_sibling.next_sibling
                        self.english.append(newer_def.text.split("\n")[0])

                        new_def = newer_def

            except AttributeError:
                pass
            else:
                pass

        except urllib2.HTTPError, e:
            print e.code

        except urllib2.URLError, e:
            print e.code

        else:
            pass


def main():
    global pages_crawled
    with codecs.open(results_file, "a", encoding="utf-8") as stream:
        with codecs.open(input_file, mode="r", encoding="utf-8") as myitems:
            items = myitems.readlines()
            for item in items:
                if item.startswith("Index"):
                    pass
                else:
                    myrow = RowInTheLexicon(item.encode('utf-8'))
                    myrow.get_lexicon_info(item.encode('utf-8')),

                    stream.write("\n%s;" % str(myrow.index)),

                    for term in myrow.searchable:

                        wiki = WiktionaryEntry(term)
                        wiki.check_page()
                        wiki.get_translation()
                        pages_crawled += 1
                        print pages_crawled

                        ## Delete some common Wiktionary entry prefixes:

                        if wiki.english_short.startswith(
                                "(Advanced Mandarin) "):
                            wiki.english_short = wiki.english_short[20:]

                        if wiki.english_short.startswith(
                                "(Elementary Mandarin) "):
                            wiki.english_short = wiki.english_short[22:]

                        if wiki.english_short.startswith(
                                "(Beginning Mandarin) "):
                            wiki.english_short = wiki.english_short[21:]

                        if wiki.english_short.startswith(u"† "):
                            wiki.english_short = wiki.english_short[2:] + \
                                                 " [obsolete]"

                        if wiki.english_short != '':
                            if not wiki.english_short.startswith(
                                    "This entry needs a definition. " \
                                    "Please add one, then remove"):
                                try:
                                    stream.write("%s (%s), " % (
                                        wiki.english_short.decode('utf-8'),
                                        term.decode('utf-8'))),
                                except UnicodeDecodeError:
                                    stream.write(
                                        "UnicodeDecodeError (%s)" % term.decode(
                                            'utf-8'))
                                except UnicodeEncodeError:
                                    stream.write(
                                        "UnicodeEncodeError (%s)" % term.decode(
                                            'utf-8'))
                                else:
                                    pass
                            else:
                                pass

                    ## wait a few seconds between searches--we don't
                    ## want to overload the server
                    delay = random.randint(0,4)
                    time.sleep(delay)

                    ## longer wait after 100 pages
                    if pages_crawled % 100:
                        long_delay = random.randint(11,29)
                        time.sleep(long_delay)

if __name__ == "__main__":
    ## counter to track the number of pages crawled
    pages_crawled = 0
    main()

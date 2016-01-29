#!/usr/bin/env python
# -*-coding=utf-8 -*-

"""TMX2QPH.

Translation Memory eXchange to Qt Phrase Book converter.

Usage:
  tmx2qph.py <file> [--source-language=<code>][--target-language=<code>] [--output=<file>]
  tmx2qph.py (-h | --help)
  tmx2qph.py --version

Options:
  -s --source-language=<code> Source language
  -t --target-language=<code> Target language
  -o --output=<file>          Output file
  -h --help                   Show this screen.
  --version                   Show version.

"""
from docopt import docopt
from bs4 import BeautifulSoup, NavigableString
from fuzzywuzzy import fuzz

def containsTooltip(phrase, theshold):
    source = phrase['source']
    target = phrase['target']
    if source.count("\\n") == 1 and target.count("\\n") == 1:
        parts = source.split('\\n')
        ratio = fuzz.partial_ratio(parts[0], parts[1])
        return ratio >= theshold
    return False
        
def separateToolTip(phrase):
    textPhrase = {}
    tooltipPhrase = {}
    if 'definition' in phrase:
        textPhrase['definition'] = phrase['definition']
        tooltipPhrase['definition'] = phrase['definition'] + " - Tooltip"
    else:
        tooltipPhrase['definition'] = "Tooltip"
        
    parts = phrase['source'].split('\\n')
    tooltipPhrase['source'] = parts[0]
    textPhrase['source'] = parts[1]
    
    parts = phrase['target'].split('\\n')
    tooltipPhrase['target'] = parts[0]
    textPhrase['target'] = parts[1]

    return (textPhrase, tooltipPhrase)

def convert(file, source, target):
    tmxSoup = BeautifulSoup(open(file, encoding='utf8'), "html.parser")

    if not source:
        for tuv in tmxSoup("tuv"):
            try:
                source = tuv['xml:lang']
                break
            except:
                pass

    if not target:
        for tuv in tmxSoup("tuv"):
            try:
                target = tuv['xml:lang']
                if target != source:
                    break
            except:
                pass

    phrases = []
    for tu in tmxSoup('tu'):
        
        phrase = {}

        if 'tuid' in tu.attrs:
            phrase['definition'] = tu['tuid']

        for tuv in tu("tuv"):
            if tuv['xml:lang'] == source and len(tuv.seg.contents) >= 1:
                phrase['source'] = tuv.seg.contents[0]
            elif tuv['xml:lang'] == target and len(tuv.seg.contents) >= 1:
                phrase['target'] = tuv.seg.contents[0]

        if 'source' in phrase and 'target' in phrase:
            if containsTooltip(phrase, 50):
                for part in separateToolTip(phrase):
                    phrases.append(part)
            else:
                phrases.append(phrase)

    qphSoup = BeautifulSoup("<!DOCTYPE QPH>", "html.parser")
    qphSoup.append(qphSoup.new_tag("QPH", sourcelanguage=source, language=target))
    for phrase in phrases:
        phraseTag = qphSoup.new_tag("phrase")
        qphSoup.QPH.append(phraseTag)

        sourceTag = qphSoup.new_tag("source")
        sourceTag.append(NavigableString(phrase["source"]))
        phraseTag.append(sourceTag)

        targetTag = qphSoup.new_tag("target")
        targetTag.append(NavigableString(phrase["target"]))
        phraseTag.append(targetTag)

        if "definition" in phrase:
            definitionTag = qphSoup.new_tag("definition")
            definitionTag.append(NavigableString(phrase["definition"]))
            phraseTag.append(definitionTag)

    
    
    return qphSoup

if __name__ == '__main__':
    import sys
    arguments = docopt(__doc__, version='TMX2QPH 0.1')

    result = convert(arguments['<file>'], arguments['--source-language'], arguments['--target-language'])
    
    if arguments['--output']:
        with open(arguments['--output'], 'w', encoding='utf8') as file:
            file.write(str(result))
    else:
        print(result.prettify().encode(sys.stdout.encoding, "replace").decode(sys.stdout.encoding, "replace"))
         
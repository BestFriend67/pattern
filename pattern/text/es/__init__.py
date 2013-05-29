#### PATTERN | ES ##################################################################################
# -*- coding: utf-8 -*-
# Copyright (c) 2012 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).
# http://www.clips.ua.ac.be/pages/pattern

####################################################################################################
# Spanish linguistical tools using fast regular expressions.

import os
import sys

try:
    MODULE = os.path.dirname(os.path.abspath(__file__))
except:
    MODULE = ""

sys.path.insert(0, os.path.join(MODULE, "..", "..", "..", ".."))

# Import parser base classes.
from pattern.text import (
    Lexicon, Spelling, Parser as _Parser, ngrams, pprint, commandline,
    PUNCTUATION
)
# Import parse tree base classes.
from pattern.text.tree import (
    Tree, Text, Sentence, Slice, Chunk, PNPChunk, Chink, Word, table,
    SLASH, WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA, AND, OR
)
# Import verb tenses.
from pattern.text import (
    INFINITIVE, PRESENT, PAST, FUTURE, CONDITIONAL,
    FIRST, SECOND, THIRD,
    SINGULAR, PLURAL, SG, PL,
    INDICATIVE, IMPERATIVE, SUBJUNCTIVE,
    IMPERFECTIVE, PERFECTIVE, PROGRESSIVE,
    IMPERFECT, PRETERITE,
    PARTICIPLE, GERUND
)
# Import inflection functions.
from pattern.text.es.inflect import (
    article, referenced, DEFINITE, INDEFINITE,
    MASCULINE, MALE, FEMININE, FEMALE, NEUTER, NEUTRAL, PLURAL,
    pluralize, singularize, NOUN, VERB, ADJECTIVE,
    verbs, conjugate, lemma, lexeme, tenses,
    predicative, attributive
)
# Import all submodules.
from pattern.text.es import inflect

sys.path.pop(0)

#--- SPANISH PARSER --------------------------------------------------------------------------------
# The Spanish parser (accuracy 92%) is based on the Spanish portion Wikicorpus v.1.0 (FDL license),
# using 1.5M words from the tagged sections 10000-15000.
# Samuel Reese, Gemma Boleda, Montse Cuadros, Lluís Padró, German Rigau. 
# Wikicorpus: A Word-Sense Disambiguated Multilingual Wikipedia Corpus. 
# Proceedings of 7th Language Resources and Evaluation Conference (LREC'10), 
# La Valleta, Malta. May, 2010. 
# http://www.lsi.upc.edu/~nlp/wikicorpus/

# The lexicon uses the Parole tagset:
# http://www.lsi.upc.edu/~nlp/SVMTool/parole.html
# http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html
PENN = PENNTREEBANK = "penntreebank"
PAROLE = "parole"
parole = {
    "AO": "JJ",   # primera
    "AQ": "JJ",   # absurdo
    "CC": "CC",   # e
    "CS": "IN",   # porque
    "DA": "DT",   # el
    "DD": "DT",   # ese
    "DI": "DT",   # mucha
    "DP": "PRP$", # mi, nuestra
    "DT": "DT",   # cuántos
    "Fa": ".",    # !
    "Fc": ",",    # ,
    "Fd": ":",    # :
    "Fe": "\"",   # "
    "Fg": ".",    # -
    "Fh": ".",    # /
    "Fi": ".",    # ?
    "Fp": ".",    # .
    "Fr": ".",    # >>
    "Fs": ".",    # ...
   "Fpa": "(",    # (
   "Fpt": ")",    # )
    "Fx": ".",    # ;
    "Fz": ".",    # 
     "I": "UH",   # ehm
    "NC": "NN",   # islam
   "NCS": "NN",   # guitarra
   "NCP": "NNS",  # guitarras
    "NP": "NNP",  # Óscar
    "P0": "PRP",  # se
    "PD": "DT",   # ése
    "PI": "DT",   # uno
    "PP": "PRP",  # vos
    "PR": "WP$",  # qué
    "PT": "WP$",  # qué
    "PX": "PRP$", # mío
    "RG": "RB",   # tecnológicamente
    "RN": "RB",   # no
    "SP": "IN",   # por
   "VAG": "VBG",  # habiendo
   "VAI": "MD",   # había
   "VAN": "MD",   # haber
   "VAS": "MD",   # haya
   "VMG": "VBG",  # habiendo
   "VMI": "VB",   # habemos
   "VMM": "VB",   # compare
   "VMN": "VB",   # comparecer
   "VMP": "VBN",  # comparando
   "VMS": "VB",   # compararan
   "VSG": "VBG",  # comparando
   "VSI": "VB",   # será
   "VSN": "VB",   # ser
   "VSP": "VBN",  # sido
   "VSS": "VB",   # sea
     "W": "NN",   # septiembre
     "Z": "CD",   # 1,7
    "Zd": "CD",   # 1,7
    "Zm": "CD",   # £1,7
    "Zp": "CD",   # 1,7%
}

def parole2penntreebank(tag):
    """ Converts a Parole tag to Penn Treebank II tag.
        For example: importantísimo AQ => importantísimo/JJ
    """
    return parole.get(tag, tag)

ABBREVIATIONS = set((
    u"a.C.", u"a.m.", u"apdo.", u"aprox.", u"Av.", u"Avda.", u"c.c.", u"D.", u"Da.", u"d.C.", 
    u"d.j.C.", u"dna.", u"Dr.", u"Dra.", u"esq.", u"etc.", u"Gob.", u"h.", u"m.n.", u"no.", 
    u"núm.", u"pág.", u"P.D.", u"P.S.", u"p.ej.", u"p.m.", u"Profa.", u"q.e.p.d.", u"S.A.", 
    u"S.L.", u"Sr.", u"Sra.", u"Srta.", u"s.s.s.", u"tel.", u"Ud.", u"Vd.", u"Uds.", u"Vds.", 
    u"v.", u"vol.", u"W.C."
))

def find_lemmata(tokens):
    """ Annotates the tokens with lemmata for plural nouns and conjugated verbs,
        where each token is a [word, part-of-speech] list.
    """
    for token in tokens:
        word, pos, lemma = token[0], token[1], token[0]
        if pos.startswith(("DT",)):
            lemma = singularize(word, pos="DT")
        if pos.startswith(("JJ",)):
            lemma = predicative(word)
        if pos == "NNS":
            lemma = singularize(word)
        if pos.startswith(("VB", "MD")):
            lemma = conjugate(word, INFINITIVE) or word
        token.append(lemma.lower())
    return tokens
    
class Parser(_Parser):

    def find_tokens(self, tokens, **kwargs):
        kwargs.setdefault("abbreviations", ABBREVIATIONS)
        kwargs.setdefault("replace", {})
        return _Parser.find_tokens(self, tokens, **kwargs)

    def find_lemmata(self, tokens, **kwargs):
        return find_lemmata(tokens)

    def find_tags(self, tokens, **kwargs):
        if kwargs.get("tagset") != PAROLE:
            kwargs.setdefault("map", parole2penntreebank)
        return _Parser.find_tags(self, tokens, **kwargs)

lexicon = Lexicon(
        path = os.path.join(MODULE, "es-lexicon.txt"), 
  morphology = os.path.join(MODULE, "es-morphology.txt"), 
     context = os.path.join(MODULE, "es-context.txt"),
    language = "es"
)
parser = Parser(
     lexicon = lexicon,
     default = ("NCS", "NP", "Z"),
    language = "es"
)

def tokenize(s, *args, **kwargs):
    """ Returns a list of sentences, where punctuation marks have been split from words.
    """
    return parser.find_tokens(s, *args, **kwargs)

def parse(s, *args, **kwargs):
    """ Returns a tagged Unicode string.
    """
    return parser.parse(s, *args, **kwargs)

def parsetree(s, *args, **kwargs):
    """ Returns a parsed Text from the given string.
    """
    return Text(parse(s, *args, **kwargs))

def split(s, token=[WORD, POS, CHUNK, PNP]):
    """ Returns a parsed Text from the given parsed string.
    """
    return Text(s, token)
    
def tag(s, tokenize=True, encoding="utf-8"):
    """ Returns a list of (token, tag)-tuples from the given string.
    """
    tags = []
    for sentence in parse(s, tokenize, True, False, False, False, encoding).split():
        for token in sentence:
            tags.append((token[0], token[1]))
    return tags

#---------------------------------------------------------------------------------------------------
# python -m pattern.es xml -s "A quien se hace de miel las moscas le comen." -OTCL

if __name__ == "__main__":
    commandline(parse)
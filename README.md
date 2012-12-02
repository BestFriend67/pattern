Pattern
=======

Pattern is a web mining module for the Python programming language. It bundles tools for:
 * Data Mining: Google + Twitter + Wikipedia API, web spider, HTML DOM parser
 * Natural Language Processing: tagger/chunker, n-gram search, sentiment analysis, WordNet
 * Machine Learning: vector space model, *k*-means clustering, Naive Bayes + *k*-NN + SVM classiﬁers
 * Network Analysis: graph centrality and visualization.

It is well documented and bundled with 30+ examples and 350+ unit tests. The source code is licensed under BSD and available from http://www.clips.ua.ac.be/pages/pattern.

![Pattern example workflow](http://www.clips.ua.ac.be/media/pattern_schema.gif)

Version
-------

2.4

License
-------

**BSD**, see `LICENSE.txt` for further details.

Installation
------------

Pattern is written for Python 2.5+ (no support for Python 3 yet). The module has no external dependencies except when using LSA in the pattern.vector module, which requires NumPy (installed by default on Mac OS X). To install Pattern so that it is available in all your scripts, unzip the download and from the command line do:
```bash
cd pattern-2.4
python setup.py install
```

If you have pip, you can automatically download and install from the PyPi repository:
```bash
pip install pattern
```

If none of the above works, you can make Python aware of the module in three ways:
- Put the pattern folder in the same folder as your script.
- Put the pattern folder in the standard location for modules so it is available to all scripts:
  * `c:\python26\Lib\site-packages\` (Windows),
  * `/Library/Python/2.6/site-packages/` (Mac OS X),
  * `/usr/lib/python2.6/site-packages/` (Unix).
- Add the location of the module to `sys.path` in your script, before importing it:

```python
  MODULE = '/users/tom/desktop/pattern'
  import sys; if MODULE not in sys.path: sys.path.append(MODULE)
  from pattern.en import parsetree
```

Documentation
-------------

http://www.clips.ua.ac.be/pages/pattern

Reference
---------

De Smedt, T., Daelemans, W. (2012). Pattern for Python. *Journal of Machine Learning Research, 13*, 2031–2035.

Contribute
----------

The source code is hosted on GitHub and contributions are welcomed. See the developer page in the documentation. There is also a donate button (PayPal) on the main documentation page. If you use Pattern in your work, please cite our reference paper.

Bundled dependencies
--------------------

Pattern is bundled with the following data sets, algorithms and Python packages:

- **Beautiful Soup**, Leonard Richardson
- **Brill tagger**, Eric Brill
- **Brill tagger for Dutch**, Jeroen Geertzen
- **Brill tagger for German**, Gerold Schneider & Martin Volk
- **Brill tagger for Spanish**, trained on Wikicorpus (Samuel Reese & Gemma Boleda et al.)
- **English pluralization**, Damian Conway
- **Spanish verb inflection**, Fred Jehle
- **Graph JavaScript framework**, Aslak Hellesoy & Dave Hoover
- **LIBSVM**, Chih-Chung Chang & Chih-Jen Lin
- **NetworkX centrality**, Aric Hagberg, Dan Schult & Pieter Swart
- **PDFMiner**, Yusuke Shinyama
- **PyWordNet**, Oliver Steele
- **simplejson**, Bob Ippolito
- **spelling corrector**, Peter Norvig
- **Universal Feed Parser**, Mark Pilgrim
- **WordNet**, Christiane Fellbaum et al.

Acknowledgements
----------------

**Authors:**

- Tom De Smedt (tom@organisms.be)
- Walter Daelemans (walter.daelemans@ua.ac.be)

**Contributors (chronological):**

- Frederik De Bleser
- Jason Wiener
- Daniel Friesen
- Jeroen Geertzen
- Thomas Crombez
- Ken Williams
- Peteris Erins
- Rajesh Nair
- F. De Smedt
- Radim Řehůřek
- Tom Loredo
- John DeBovis
- Thomas Sileo
- Gerold Schneider
- Martin Volk
- Samuel Joseph
- Shubhanshu Mishra
- Robert Elwell
- Fred Jehle
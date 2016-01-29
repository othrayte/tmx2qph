TMX2QPH
=======

A tool to convert Translation Memory eXchange (.tmx) files into Qt Phrase Books (.qph).

These phrase books can then be used in Qt Linguist to batch translate identical source strings into the target translation or to provide suggestions of translations.

Setup
-----

This tool expects Python 3, it was developed against Python 3.5.

If using VisualStudio you should add a new Python3 virtual environment from the context menu of 'Python Enviroments' in the solution explorer. This should detect the 'requirements.txt' file and install the dependencies.

Usage
-----

`tmx2qph.py <file> [--source-language=<code>][--target-language=<code>] [--output=<file>]`

Omitting the source or tartget language will result in the tool picking the missing languages from the ones provided in the tmx file with the source picked before the target language. For simple tmx files that only contain two languages desired and where the source comes first these parameters can be omitted. If the order is different then specifying one of the two is sufficient to get the correct result.

Omitting the output file results in the qph data being written to stdout, this should be suitable for piping to other programs but is limited to the consoles support for utf8 encoding; as a result some charactors may not be able to be written.

The resulting qph Phrase book can be used in Qt Linguist, see http://doc.qt.io/qt-4.8/linguist-translators.html#phrase-books.

Tooltips
--------

The tool interprets text in the form `"Open a new file\nOpen"` as a tooltip followed by the action and splits them into two translations. This only occurs when their is exactly one `'\n'` in the source and where the two halves have at least a 50% match.

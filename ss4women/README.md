How to use this parser
======================

First use pdftotext (this is a classic linux tool and can be downloaded for mac
[here](http://www.wesselvalkenburg.nl/software/pdftotext/).

Use this as follows: `$ pdftotext [name_of_file] -layout`. In this case the name
of the file should be the name of the pdf. This will create a text file with the
same name (different extension).

For this file, I also deleted every line of the converted pdf after 8846. All
lines after this are no longer related to specific nonprofits. One can do this
processing using `$ head -8846 [name_of_file] > [name_of_cleaned_file]`. I called
the new, cleaned file directory.txt

Now you can use the parser. Use this as `$ python scraper.py
[name_of_cleaned_file] > [name_of_csv]`

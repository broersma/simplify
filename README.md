Installation
============

simplify.py depends on networkx>=1.7.0 which can be installed from PyPI using pip:

$ pip install networkx

or setuptools:

$ easy_install networkx

Usage
=====

With an input text file:
```
$ python simplify.py < input.txt
```
or using standard input:

```
$ python simplify.py
John owes Bill $40.00
Bill owes John $20.00
^Z
```

Notes
=====

Names should take the format of a list of non-whitespace characters, starting with an uppercase character. Like so: `Bill`

Amounts of money are written as floating point numbers with two digits behind the point, which can be either a period or a comma. Like `4.99` or `1,25`.

Each line should contain exactly two names and one monetary sum. Empty lines are ignored. Other lines throw an error.

The program's output format is taken from the first line. So the second usage example should return `John owes Bill $20.00`.
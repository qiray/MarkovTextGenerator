# Markov Text Generator

Text generator using Markov chain to generate pseudo meaningful text.

## Requirements

This program uses Python 3 and some extra libraries:

- argparse to parse command line arguments;

- NLTK to parse text files and sentences.

## Installation

You should install requirements to use this program: python3, pip3 and some additional python libraries. There is requirements.txt file with libraries' list.

Before using this program you should install some nltk data. It's pretty simple - just run:

``` bash
python3 prepare.py
```

## Usage

```
python3 main.py [OPTIONS]

-h, --help            show this help message and exit
--init                Init database only
-f PARSE, --parse PARSE
                      Parse text file and save it in database
-n NUMBER, --number NUMBER
                      Set size of token for text parsing (default = 3)
-g, --generate        Generate text sequence
-v, --version         Show version
--differentsource     Enable this option to generate texts from different
                      sources only
```

For example, to parse text file file.txt and add it's content to database:
``` bash
python3 main.py -f file.txt
```
To generate a sentence using existing database run:
``` bash
python3 main.py -g
```
```

### License
This program uses GNU GPL3. For more information see the LICENSE file.

# Markov Text Generator

Text generator using Markov chain to generate pseudo meaningful text.

## Requirements

This program uses Python 3 and some extra libraries:

- argparse to parse command line arguments;

- NLTK to parse text files and sentences;

- tweepy to post tweets.

## Installation

You should install requirements to use this program: python3, pip3. and additional python libraries. On *NIX systems you can simply run this code:

``` bash
bash dependecies.sh
```

Or you can manually install dependencies.

In bash:

``` bash
pip3 install nltk
pip3 install argparse
pip3 install tweepy
```

And in python:

``` python
import nltk
nltk.download('punkt')
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
-t, --tweet           Tweet generated sentence
--favorite            Add to favorites posted tweet
--differentsource     Use different sources only
```

For example, to parse text file file.txt and add it's content to database:
``` bash
python3 main.py -f file.txt
```
To generate a sentence using existing database run:
``` bash
python3 main.py -g
```
To genereate a sentence and post it to Twitter:
``` bash
python3 main.py -g -t
```
For tweets you need to edit file secrets.py adding config with real data:

``` python
cfg = { 
    "consumer_key"        : "consumer_key",
    "consumer_secret"     : "consumer_secret",
    "access_token"        : "access_token",
    "access_token_secret" : "access_token_secret"
}
```

### License
This plugin uses GNU GPL3. For more information see the LICENSE file.

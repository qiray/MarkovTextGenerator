#!/bin/bash

pip3 install nltk
pip3 install argparse
pip3 install tweepy

PYTHON_CODE=$(cat <<END
import nltk
nltk.download('punkt')
END
)

# use the 
python3 -c "$PYTHON_CODE"

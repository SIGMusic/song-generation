# using python2.7 because Text.generate doesn't exist on NLTK 3.0
import nltk
from nltk import trigrams
from nltk import Text

# this is for when we have a small corpus (one song)
import warnings 
warnings.simplefilter('ignore') 

# we have lyrics stored in variable called lyrics
# based off of http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
def analyze(lyrics):
  words_to_generate = 100
  tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
  content_text = ' '.join(lyrics)
  tokenized_content = tokenizer.tokenize(content_text)
  content_model = nltk.NgramModel(3, tokenized_content)

  starting_words = content_model.generate(100)[-2:]
  content = content_model.generate(words_to_generate, starting_words)
  print(' '.join(content))

with open('pg1342.txt') as f:
  lyrics = f.readlines()
analyze(lyrics)
# analyze(azlyrics_scrape.lyrics)
# Write your code here
import random
import nltk, re, pprint, string
from nltk import word_tokenize, sent_tokenize, WhitespaceTokenizer
from nltk.util import ngrams
from nltk.corpus import stopwords
from collections import Counter, defaultdict


def isword(word):
    pattern = r'\A[A-Z].*[ˆ\w\s]\Z'
    return bool(re.match(pattern, word) is not None)

def listgoodwords(words):
    goods = list()
    for g in words:
        if isword(g):
            goods.append(g)
    return goods

def isgoodsentence(sentence):
    pattern = r'\A[A-Z].*[?.!]\Z'#'^[A-Z][ˆ\w\s]*[?.!]$'
    if 4<= len(re.findall(r"\s",sentence)):
        return bool(re.match(pattern, sentence) is not None)#'^[A-Z].*[?.!]$'
    else:
        return False

def getrandomWord(wordlist):
  return random.choices(listgoodwords(wordlist))[0]

def gethead(head,tail=''):
  if len(tail)==0:
    _head = head
  else:
    _head = f'{head.split()[-1]} {tail}'
  return _head

#string.punctuation = string.punctuation +'“'+'”'+'-'+'’'+'‘'+'—'
#string.punctuation = string.punctuation.replace('.', '')
#string.punctuation = string.punctuation.replace('!', '')
#string.punctuation = string.punctuation.replace('?', '')

file = input()
file = open(file, encoding = 'utf8').read()
#preprocess data
#file_nl_removed = ""
#for line in file:
#  line_nl_removed = line.replace("\n", " ")      #removes newlines
#  file_nl_removed += line_nl_removed
#file_p = "".join([char for char in file_nl_removed if char not in string.punctuation])
words = WhitespaceTokenizer().tokenize(file)
trigram = list(ngrams(words, 3))
stop_words = set(stopwords.words('english'))

freq_tri = nltk.FreqDist(trigram)

trigHeadTail = defaultdict(str)
for t in trigram:
    h = f'{t[0]} {t[1]}'
    trigHeadTail[h] = t[2]

freq_head = []
for word in [[key for key in item[0]] for item in list(freq_tri.most_common(100))]:
  h = f'{word[0]} {word[1]}'
  freq_head.append(h)
freq_head = list(set(freq_head))
first = getrandomWord(freq_head)

outs = []
head = gethead(first)
tail = trigHeadTail[head]
out = head +" "+ tail
count = 0
while True:
  if isgoodsentence(out):
    print(out)
    head = getrandomWord(freq_head)#gethead(head,tail)
    tail = trigHeadTail[head]
    out = head +" "+ tail
    count+=1
  else:
    head = gethead(head,tail)
    tail = str(trigHeadTail[head])
    out+=" "+tail
  if count>=10:
    break
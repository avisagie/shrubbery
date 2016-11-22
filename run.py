import os
import nltk
import re

# these are simply stripped of their .
# Find them using abbrs.py
abbreviations = [
    'mnr.',
    'Mnr.',
    'mnre.',
    'Mnre.',
    'MNR.',
    'MNRe.',

    'adv.',

    'kapt.'
    'Kapt.'
    'Kol.'
    'kol.'

    'ds.',
    'Dr.',
    'dr.',
    
    'mev.',
    'Mev.',
    'meve.',
    'Meve.',

    'mej.',
    'Mej.',

    'P.W.',
    'F.W.',
    'pres.',
    'Pres.',
    'bl.',

    'st.',
    'St.',
]


abbr_re = [
    re.compile(r'(?:[A-Z]\.)+'),
]


# process a file
def process(filename):
    # TODO ponder removing accents e.g. nié
    # break them into sentences
    with open(filename) as fid:
        text = fid.read()

    print(len(text), 'characters of text')

    # Replace all known common abbreviations. This is horribly
    # inefficient. Better would be to train a proper Afrikaans
    # sentence breaker.
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '_'))
    for abbr in abbr_re:
        text = abbr.sub('A_B_B_R_', text)

    # http://www.nltk.org/api/nltk.tokenize.html
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_detector.tokenize(text)    
    print(len(sentences), 'sentences')
    with open(filename+'.sentences', 'w') as fid:
        for sentence in sentences:
            fid.write(sentence.replace('\r','').replace('\n', ' ') + '\n')


    with open(filename + '.nie', 'w') as out:
        # find those with nie, count them
        # TODO deal with nooit, niks, geen etc.
        nie = re.compile(r'[^A-Za-z]nie[^A-Za-z]')
        for sentence in sentences:
            m = nie.findall(' ' + sentence + ' ')
            if not m: continue
            out.write(str(len(m)) + ": " + sentence + '\n')

    return 
            

# Download the punkt tokenizers from the Models tab. Comment the next
# line out when it starts to bug you.
nltk.download()
    
# loop over files
final_token_counts = {}
for path, dirs, files in os.walk('./data/'):
    for fn in files:
        if fn.lower().endswith('.txt'):
            fullname = os.path.join(path, fn)
            print('processing', fullname)
            final_tokens = process(fullname)


print("press enter to exit")
input('> ')

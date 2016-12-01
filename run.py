import os
import nltk
import re
import gzip
import sys

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

    'kapt.',
    'Kapt.',
    'Kol.',
    'kol.',
    'genl.',

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

    'tel.',
    'nr.',
    
    'ens.',
    'bv.',
]

# Spot abbreviations like A.B.C.
abbr_re = [
    re.compile(r'(?:[A-Z]\.)+'),
]

# Afrikaans words that count as a "nie"
nie_words = [x.strip() for x in """
nie
moenie
geen
g[']n
niks
niemand
nerens
nêrens
nooit
geeneen
geensins
""".split()]

# Set to True to include [-> <-] markers for the matched words. Useful
# for debugging.
mark_matches = False

# pre-processing replacements.
preproc_replacements = [
    # Some BEELD files have this.
    re.compile(r'Geen Titel'),
]

# process a file
def process(filename):
    # TODO ponder removing accents e.g. nié
    # break them into sentences
    if filename.endswith('.txt'):
        with open(filename, 'rb') as fid:
            text = fid.read()
    elif filename.endswith('.gz'):
        with gzip.open(filename) as fid:
            text = fid.read()

    text = text.decode('latin-1', errors='replace')
    print(len(text), 'characters of text')

    # Replace all known common abbreviations. This is horribly
    # inefficient. Better would be to train a proper Afrikaans
    # sentence breaker.
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace('.', '_'))
    for abbr in abbr_re:
        text = abbr.sub('A_B_B_R_', text)
    for p in preproc_replacements:
        text = p.sub('', text)

    # http://www.nltk.org/api/nltk.tokenize.html
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentence_detector.tokenize(text)    
    print(len(sentences), 'sentences')
    sys.stdout.flush()

    nie_fids = [open(filename + '.' + str(x+1) + '.nie', 'w', encoding='utf-8') for x in range(0,4)]
    
    with open(filename+'.sentences', 'w', encoding='utf-8') as fid_sentences:
        # find those with nie, count them
        # TODO deal with nooit, niks, geen etc.
        nie = re.compile(r'([^A-Za-z])(' + "|".join(nie_words) + ')(?=[^A-Za-z-])', re.IGNORECASE)
        print(nie.pattern)
        for sentence in sentences:
            s = ' ' + sentence.replace('\r','').replace('\n', ' ') + ' '
            m = nie.findall(s)
            if m:
                fid_sentences.write(str(len(m)) + ':' + s + '\n')
                if mark_matches:
                    s = nie.sub('\\1[->\\2<-]', s)
                if len(m) <= len(nie_fids):
                    nie_fids[len(m)-1].write(s + '\n')
            else:
                fid_sentences.write('0:' + s + '\n')
            
    return 
            
    
# loop over files
final_token_counts = {}
for path, dirs, files in os.walk('./data/'):
    for fn in files:
        if fn.lower().endswith('.txt') or fn.lower().endswith('.txt.gz'):
            fullname = os.path.join(path, fn)
            print('processing', fullname)
            sys.stdout.flush()
            final_tokens = process(fullname)
            sys.stdout.flush()


print("press enter to exit")
input('> ')

import re
import os

de = re.compile(r'\S+\.')
def extract(filename):
    with open(filename) as fid:
        text = fid.read()

    return de.findall(text)


dotendercounts = {}
for path, dirs, files in os.walk('./data/'):
    for fn in files:
        if fn.lower().endswith('.txt'):
            fullname = os.path.join(path, fn)
            dotenders = extract(fullname)
            for t in dotenders:
                dotendercounts[t] = dotendercounts.get(t, 0) + 1

dotendercounts = [(y,x) for x,y in dotendercounts.items()]
dotendercounts.sort()
dotendercounts.reverse()

for y,x in dotendercounts[:100]:
    print(y,x)

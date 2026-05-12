import sys, urllib.request, urllib.parse, json, os

def translate(text, target='en'):
    url = ('https://translate.googleapis.com/translate_a/single'
           '?client=gtx&sl=auto&tl=' + target + '&dt=t&q=' + urllib.parse.quote(text))
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())
        return ''.join([p[0] for p in data[0] if p[0]])

text = ' '.join(sys.argv[1:])
print(translate(text))

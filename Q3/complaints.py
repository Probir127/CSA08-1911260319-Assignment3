"""Normalize words, count by get/setdefault/Counter and group complaints."""
from collections import Counter
from pathlib import Path
from time import perf_counter
import json
STOP={'the','not','and','is','high'}
def words(text):
    """Lowercase and turn punctuation/nonletters into word separators."""
    return ''.join(c.lower() if c.isalpha() else ' ' for c in text).split()
def dict_get(tokens):
    """Count each supplied token with dict.get."""
    result={}
    for word in tokens:result[word]=result.get(word,0)+1
    return result
def dict_setdefault(tokens):
    """Count using setdefault; grouping below also demonstrates its natural use."""
    result={}
    for word in tokens:result.setdefault(word,0);result[word]+=1
    return result
def list_count(tokens):
    """Scan the token list once per distinct word."""
    return {word:tokens.count(word) for word in set(tokens)}
def group(records):
    """Return district and crop dictionaries of original complaint records."""
    district={};crop={}
    for record in records:
        district.setdefault(record['district'],[]).append(record)
        crop.setdefault(record['crop'],[]).append(record)
    return district,crop
if __name__=='__main__':
    sample=[dict(district='Chennai',crop='rice',text='SEEDS, seeds! delayed.'),
            dict(district='Madurai',crop='rice',text='Price is HIGH; seeds.'),
            dict(district='Chennai',crop='millet',text='')]
    district,crop=group(sample)
    assert {key:len(value) for key,value in district.items()}=={'Chennai':2,'Madurai':1}
    assert len(crop['rice'])==2
    tokens=[w for r in sample for w in words(r['text']) if w not in STOP]
    assert dict_get(tokens)==dict_setdefault(tokens)==dict(Counter(tokens))=={'seeds':3,'delayed':1,'price':1}
    assert dict_get([])==list_count([])=={}
    print('District counts:',{k:len(v) for k,v in district.items()})
    print('Crop groups:',{k:len(v) for k,v in crop.items()})
    print('Case/punctuation/empty checks PASS:',dict_get(tokens))
    templates=['seeds not received seeds delayed','fertiliser price high',
               'seeds price high subsidy not received','water pump broken crop drying']
    results=[]
    for n in [1000,10000,100000]:
        texts=[templates[i%len(templates)] for i in range(n)]
        tokens=[w for text in texts for w in words(text) if w not in STOP]
        row={'complaints':n,'words':len(tokens),'distinct':len(set(tokens)),'seconds':{}}
        answers=[]
        for fn in [dict_get,dict_setdefault,list_count,Counter]:
            begin=perf_counter();answer=dict(fn(tokens));row['seconds'][fn.__name__]=perf_counter()-begin;answers.append(answer)
        assert all(answer==answers[0] for answer in answers)
        row['list_count_comparisons_model']=len(tokens)*len(set(tokens))
        results.append(row)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

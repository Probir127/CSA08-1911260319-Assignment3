"""Merge connected contacts using shared canonical phone numbers, not names."""
import re,json
from pathlib import Path
from time import perf_counter
def phone(raw):
    """Assume Indian 10-digit numbers; accept +91/0091 and benign separators."""
    text=str(raw).strip()
    if any(c not in '0123456789+ -().' for c in text):return None
    if text.count('+')>1 or ('+' in text and not text.startswith('+91')):return None
    digits=''.join(c for c in text if c in '0123456789')
    if digits.startswith('0091') and len(digits)==14:digits=digits[4:]
    elif digits.startswith('91') and len(digits)==12:digits=digits[2:]
    if len(digits)!=10:return None
    return '+91'+digits
def name(raw):
    """Normalize display aliases; names alone never imply identity."""
    parts=re.sub(r'[^\w\s]',' ',str(raw or '').casefold()).split()
    if parts and parts[0] in {'dr','mr','mrs','ms'}:parts=parts[1:]
    return ' '.join(parts)
def prepare(records):
    """Canonicalize fields; invalid phones are omitted and flagged."""
    result=[]
    for i,record in enumerate(records):
        if not isinstance(record,dict):raise ValueError('Contact must be a dictionary')
        numbers=set();invalid=[]
        for raw in record.get('numbers',[]) or []:
            normalized=phone(raw)
            if normalized:numbers.add(normalized)
            else:invalid.append(str(raw))
        emails={str(e).strip().casefold() for e in (record.get('emails',[]) or []) if str(e).strip()}
        alias=name(record.get('name',''))
        result.append(dict(names={alias} if alias else set(),numbers=numbers,emails=emails,invalid_numbers=invalid,source_ids={i}))
    return result
def combine(prepared,root):
    """Gather connected records into deterministic, JSON-friendly reports."""
    groups={}
    for i,record in enumerate(prepared):
        group=groups.setdefault(root(i),dict(names=set(),numbers=set(),emails=set(),source_ids=set(),invalid_numbers=[]))
        for field in ['names','numbers','emails','source_ids']:group[field].update(record[field])
        group['invalid_numbers'].extend(record['invalid_numbers'])
    output=[]
    for group in groups.values():output.append({key:sorted(value) for key,value in group.items()})
    return output  # Groups are first encountered in original input order.
def structure(n):
    """Union-find with path compression and union by size handles bridge records."""
    parents=list(range(n));sizes=[1]*n
    def find(i):
        """Return root and compress paths."""
        while parents[i]!=i:
            parents[i]=parents[parents[i]];i=parents[i]
        return i
    def union(a,b):
        """Join components, attaching the smaller tree to the larger."""
        a,b=find(a),find(b)
        if a==b:return
        if sizes[a]<sizes[b]:a,b=b,a
        parents[b]=a;sizes[a]+=sizes[b]
    return find,union
def merge(records):
    """Dictionary number -> representative; union every shared-number edge."""
    prepared=prepare(records);find,union=structure(len(prepared));owner={};lookups=0
    for i,record in enumerate(prepared):
        for number in record['numbers']:
            lookups+=1
            if number in owner:union(i,owner[number])
            else:owner[number]=i
    return combine(prepared,find),lookups
def pairwise(records,checkpoint=None):
    """Every-pair reference; optional progress callback counts attempted comparisons."""
    prepared=prepare(records);find,union=structure(len(prepared));comparisons=0
    for i in range(len(prepared)):
        for j in range(i):
            comparisons+=1
            if prepared[i]['numbers'] & prepared[j]['numbers']:union(i,j)
            if checkpoint and comparisons%100000==0:checkpoint(comparisons)
    return combine(prepared,find),comparisons
def generated(n):
    """Five formatted records per person, with a bounded phone field size."""
    records=[]
    for i in range(n):
        person=i//5;digits=f'{9000000000+person:010d}'
        written='+91 '+digits[:5]+' '+digits[5:] if i%2 else digits
        records.append(dict(name=f'Person {person}',numbers=[written],emails=[f'p{person}@example.test']))
    return records
def fixture():
    """Synthetic examples include a bridge, same names and missing fields."""
    return [dict(name='Dr. Ravi',numbers=['+91 98400 12345'],emails=['RAVI@example.test']),
            dict(name='ravi kumar',numbers=['9840012345','9876543210'],emails=['ravi.work@example.test']),
            dict(name='R. Kumar',numbers=['0091 9876543210'],emails=[]),
            dict(name='ravi kumar',numbers=['9123456789'],emails=[]),
            dict(name='No Phone',emails=['solo@example.test']),
            dict(name='',numbers=['invalid'])]
if __name__=='__main__':
    sample=fixture();actual,lookups=merge(sample);reference,comparisons=pairwise(sample)
    assert actual==reference and len(actual)==4
    assert actual[0]['source_ids']==[0,1,2] and len(actual[0]['numbers'])==2 and len(actual[0]['emails'])==2
    assert actual[1]['source_ids']==[3] and actual[2]['source_ids']==[4] and actual[3]['source_ids']==[5]
    assert merge([])==([],0)
    assert phone('+91 98400 12345')==phone('0091 9840012345')=='+919840012345'
    bridge=[{'numbers':['9000000001']},{'numbers':['9000000002']},{'numbers':['9000000001','9000000002']}]
    assert len(merge(bridge)[0])==1 and merge(bridge)[0]==pairwise(bridge)[0]
    print('Hand fixture groups, aliases, same-name separation, bridge and empty tests PASS')
    print(json.dumps(actual,indent=2))
    Path(__file__).with_name('sample_input.json').write_text(json.dumps(sample,indent=2))
    Path(__file__).with_name('sample_output.json').write_text(json.dumps(actual,indent=2))
    rows=[]
    for n in [1000,100000]:
        records=generated(n);begin=perf_counter();groups,count=merge(records);elapsed=perf_counter()-begin
        assert len(groups)==n//5 and sum(len(g['source_ids']) for g in groups)==n
        row=dict(n=n,groups=len(groups),dictionary_seconds=elapsed,phone_occurrences=count,required_pair_comparisons=n*(n-1)//2)
        if n==1000:
            begin=perf_counter();other,comp=pairwise(records);row['pairwise_seconds']=perf_counter()-begin
            assert other==groups and comp==n*(n-1)//2
        rows.append(row)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows,indent=2))

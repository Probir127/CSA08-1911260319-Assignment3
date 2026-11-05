"""Weekly summaries and instrumented seven-day moving averages."""
import random,json,math
from pathlib import Path
from time import perf_counter
def naive(values,k=7):
    """Return averages and explicit additions, using one slice per window."""
    if k<=0:raise ValueError('Positive window required')
    result=[];adds=0
    for start in range(len(values)-k+1):
        total=0
        for value in values[start:start+k]:total+=value;adds+=1
        result.append(total/k)
    return result,adds
def running(values,k=7):
    """Update one total per shifted window; count additions and subtractions."""
    if k<=0:raise ValueError('Positive window required')
    if len(values)<k:return [],0,0
    total=0;adds=0;subs=0
    for value in values[:k]:total+=value;adds+=1
    result=[total/k]
    for i in range(k,len(values)):
        total-=values[i-k];subs+=1
        total+=values[i];adds+=1
        result.append(total/k)
    return result,adds,subs
def weekly(values):
    """Include a final partial week; ties are reported at every position."""
    totals=[sum(values[i:i+7]) for i in range(0,len(values),7)]
    if not totals:return {'totals':[],'wettest':[],'driest':[],'dry_days':[]}
    highest,lowest=max(totals),min(totals)
    return dict(totals=totals,wettest=[i+1 for i,v in enumerate(totals) if v==highest],
                driest=[i+1 for i,v in enumerate(totals) if v==lowest],
                dry_days=[i+1 for i,v in enumerate(values) if v==0])
def deque_average(values,k=7):
    """Streaming alternative retaining at most k readings."""
    from collections import deque
    window=deque(maxlen=k);total=0;result=[]
    for value in values:
        if len(window)==k:total-=window[0]
        window.append(value);total+=value
        if len(window)==k:result.append(total/k)
    return result
if __name__=='__main__':
    sample=[0,1,2,3,4,5,6,7,0,0,0,0,0,0]
    assert weekly(sample)['totals']==[21,7]
    assert weekly(sample)['wettest']==[1] and weekly(sample)['driest']==[2]
    assert running(sample)[0]==naive(sample)[0]==deque_average(sample)
    for values in [[],[1,2,3],[0]*7]:assert naive(values)[0]==running(values)[0]==deque_average(values)
    rows=[]
    for n in [365,36500,365000]:
        rng=random.Random(1911260319)
        # Integer millimetres deliberately make running sums exact.
        data=[rng.randrange(0,101) if rng.random()>.2 else 0 for _ in range(n)]
        begin=perf_counter();a,adds1=naive(data);t1=perf_counter()-begin
        begin=perf_counter();b,adds2,subs=running(data);t2=perf_counter()-begin
        assert a==b and adds1==7*(n-6) and adds2==n and subs==n-7
        rows.append(dict(n=n,windows=len(a),naive_additions=adds1,running_additions=adds2,
                         running_subtractions=subs,naive_seconds=t1,running_seconds=t2))
        if n==365:
            summary=weekly(data)
            Path(__file__).with_name('year_summary.json').write_text(json.dumps(summary,indent=2))
            print('365-day weekly totals:',summary['totals'])
            print('Wettest weeks:',summary['wettest'],'driest weeks:',summary['driest'])
            print('Dry days:',summary['dry_days'])
    Path(__file__).with_name('measurements.json').write_text(json.dumps(rows,indent=2))
    print('Hand sample weekly totals [21, 7], moving averages, empty/short inputs PASS')
    print(json.dumps(rows,indent=2))

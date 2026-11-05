"""Equivalent temperature cleaning pipelines retaining original minute indices."""
import random,sys,json
from pathlib import Path
from time import perf_counter
def loop(readings):
    """Filter, convert and collect alarm minutes with explicit append operations."""
    c=[];f=[];alarms=[]
    for minute,value in enumerate(readings,1):
        if -50<=value<=50:
            c.append(value);f.append(value*9/5+32)
            if not 2<=value<=8:alarms.append(minute)
    return c,f,alarms
def comprehension(readings):
    """Use list comprehensions and enumerate over the original sequence."""
    c=[value for value in readings if -50<=value<=50]
    f=[value*9/5+32 for value in c]
    alarms=[minute for minute,value in enumerate(readings,1) if -50<=value<=50 and not 2<=value<=8]
    return c,f,alarms
def functional(readings):
    """Use filter/map with lambdas and preserve original indices for alarms."""
    c=list(filter(lambda value:-50<=value<=50,readings))
    f=list(map(lambda value:value*9/5+32,c))
    alarms=list(map(lambda pair:pair[0],filter(lambda pair:-50<=pair[1]<=50 and not 2<=pair[1]<=8,enumerate(readings,1))))
    return c,f,alarms
if __name__=='__main__':
    sample=[-51,-50,2,8,9,50,51]
    expected=([-50,2,8,9,50],[-58.0,35.6,46.4,48.2,122.0],[2,5,6])
    for fn in [loop,comprehension,functional]:assert fn(sample)==expected
    for data in [[],[2,3,8],[-50,50],[-51,51,100]]:
        assert loop(data)==comprehension(data)==functional(data)
    indexed={i:c for i,c in enumerate(sample,1) if -50<=c<=50}
    distinct={c for c in sample if -50<=c<=50}
    assert indexed=={2:-50,3:2,4:8,5:9,6:50}
    print('Sample Celsius/Fahrenheit/alarm minutes:',expected)
    print('Dictionary comprehension:',indexed,'set comprehension:',sorted(distinct))
    print('Empty/all-valid/all-invalid/boundary tests PASS')
    rows=[]
    for n in [10000,100000,1000000]:
        rng=random.Random(1911260319);values=[rng.randint(-60,60) for _ in range(n)]
        row={'n':n,'seconds':{}};reference=None
        for fn in [loop,comprehension,functional]:
            begin=perf_counter();actual=fn(values);row['seconds'][fn.__name__]=perf_counter()-begin
            if reference is None:reference=actual
            else:assert actual==reference
        materialized=[c for c in values if -50<=c<=50]
        generator=(c for c in values if -50<=c<=50)
        row['valid_count']=len(materialized)
        row['list_shallow_bytes']=sys.getsizeof(materialized);row['generator_shallow_bytes']=sys.getsizeof(generator)
        begin=perf_counter();a=sum(materialized);row['sum_list_seconds']=perf_counter()-begin
        begin=perf_counter();b=sum(generator);row['sum_generator_seconds']=perf_counter()-begin
        assert a==b
        rows.append(row)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows,indent=2))

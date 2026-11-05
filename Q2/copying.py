"""Aliasing, nested copies, tuple keys and equivalent size/timing experiments."""
import copy,sys,json,random
from pathlib import Path
from time import perf_counter
from statistics import mean
def mutate(values):
    """Mutate the same object that the caller passed."""
    values.append(9)
if __name__=='__main__':
    bad=[[0]*3]*3;good=[[0]*3 for _ in range(3)]
    print('bad row ids:',[id(row) for row in bad])
    print('good row ids:',[id(row) for row in good])
    assert bad[0] is bad[1] and good[0] is not good[1]
    original=[[1],[2]];alias=original;sliced=original[:];shallow=copy.copy(original);deep=copy.deepcopy(original)
    original[0].append(7)
    assert alias is original and sliced is not original and shallow is not original
    assert sliced[0] is original[0] and shallow[0] is original[0] and deep==[[1],[2]]
    print('After nested edit: original=',original,'alias=',alias,'slice=',sliced,'shallow=',shallow,'deep=',deep)
    coordinates={(13.0827,80.2707):'Central',(13.0418,80.2341):'T. Nagar'}
    for (latitude,longitude),name in coordinates.items():print(name,latitude,longitude)
    try:coordinates[[13.0418,80.2341]]='invalid'
    except TypeError as error:print('List key rejected:',error)
    else:raise AssertionError('List key accepted')
    inside=([1,2],'stop');inside[0].append(3);assert inside==([1,2,3],'stop')
    try:hash(inside)
    except TypeError:print('Tuple containing a list is also unhashable')
    else:raise AssertionError('Mutable tuple member hashable')
    caller=[];mutate(caller);assert caller==[9]
    n=1000000;lists=[];tuples=[]
    for _ in range(3):
        begin=perf_counter();a=list(range(n));lists.append(perf_counter()-begin)
        begin=perf_counter();b=tuple(range(n));tuples.append(perf_counter()-begin)
    assert a==list(b)
    positions=[random.Random(i).randrange(n) for i in range(10000)]
    access={}
    for name,values in [('list',a),('tuple',b)]:
        times=[]
        for _ in range(3):
            begin=perf_counter();total=sum(values[i] for i in positions);times.append(perf_counter()-begin)
        access[name]={'runs_seconds':times,'mean_seconds':mean(times),'checksum':total}
    assert access['list']['checksum']==access['tuple']['checksum']
    result=dict(n=n,list_shallow_bytes=sys.getsizeof(a),tuple_shallow_bytes=sys.getsizeof(b),
                list_creation_runs=lists,tuple_creation_runs=tuples,indexing=access)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

"""Set operations, membership timing and equivalent intersection algorithms."""
import json,sys
from pathlib import Path
from time import perf_counter
def nested(a,b):
    """Compare every pair, returning distinct common values and comparison count."""
    result=set();comparisons=0
    for x in a:
        for y in b:
            comparisons+=1
            if x==y:result.add(x)
    return result,comparisons
def sorted_walk(a,b):
    """Sort and advance pointers through both lists."""
    a=sorted(a);b=sorted(b);i=j=0;result=set()
    while i<len(a) and j<len(b):
        if a[i]==b[j]:result.add(a[i]);i+=1;j+=1
        elif a[i]<b[j]:i+=1
        else:j+=1
    return result
if __name__=='__main__':
    a={'192311001','192311004','192311007','192311009'}
    b={'192311002','192311004','192311009','192311010'}
    universe={f'1923110{i:02d}' for i in range(1,11)}
    assert a.intersection(b)==a&b
    assert a.symmetric_difference(b)==a^b
    assert universe.difference(a.union(b))==universe-(a|b)
    assert a&b=={'192311004','192311009'}
    for x,y in [(set(),set()),(a,a),(a,set())]:
        assert nested(list(x),list(y))[0]==x&y==sorted_walk(list(x),list(y))
    assert set(['x','x','y'])=={'x','y'}
    print('Operator/method equality, hand case, duplicates, empty and identical sets PASS')
    membership=[]
    for n in [10000,100000,1000000]:
        values=[f'{i:010d}' for i in range(n)];lookup=set(values)
        probes=[values[-1],'missing']*10;row={'n':n,'probes':len(probes)}
        checks=[]
        for label,container in [('list',values),('set',lookup)]:
            begin=perf_counter();answers=[value in container for value in probes];row[label+'_seconds']=perf_counter()-begin;checks.append(answers)
        assert checks[0]==checks[1]
        row['set_shallow_bytes']=sys.getsizeof(lookup);membership.append(row)
    common=[]
    for n in [100,1000,3000]:
        a=list(range(n));b=list(range(n//2,n+n//2));row={'n':n,'m':len(b)}
        begin=perf_counter();old,count=nested(a,b);row['nested_seconds']=perf_counter()-begin
        begin=perf_counter();new=set(a)&set(b);row['set_seconds']=perf_counter()-begin
        begin=perf_counter();third=sorted_walk(a,b);row['sort_walk_seconds']=perf_counter()-begin
        assert old==new==third
        row['comparisons']=count;row['common']=len(new);common.append(row)
    data={'membership':membership,'intersection':common}
    Path(__file__).with_name('measurements.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))

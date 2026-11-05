"""Fictional same-day timetables with a station-to-stop index."""
import json,sys
from pathlib import Path
from time import perf_counter
DAYS={'Mon','Tue','Wed','Thu','Fri','Sat','Sun'}
def fixture():
    """Five illustrative trains, not a real railway service schedule."""
    return {
      'T101':dict(name='Village Link',stops=[('North','08:00','08:05'),('Central','09:00','09:05'),('South','10:00','10:05')],days={'Mon','Wed','Fri'}),
      'T102':dict(name='City Connector',stops=[('East','07:00','07:05'),('Central','08:30','08:35'),('West','10:00','10:05')],days=set(DAYS)),
      'T103':dict(name='Coastal Local',stops=[('Central','11:00','11:05'),('Beach','12:00','12:05'),('Port','13:00','13:05')],days={'Sat','Sun'}),
      'T104':dict(name='Valley Link',stops=[('Hill','06:00','06:05'),('Central','07:00','07:05'),('Lake','08:00','08:05')],days={'Mon','Tue'}),
      'T105':dict(name='Market Local',stops=[('North','12:00','12:05'),('Market','13:00','13:05'),('South','14:00','14:05')],days=set(DAYS)),
    }
def scan(data,station,day):
    """Visit all stops, retain running-day matches and sort by departure."""
    result=[]
    for train,info in data.items():
        for stop,arr,dep in info['stops']:
            if stop==station and day in info['days']:result.append((train,info['name'],arr,dep))
    return sorted(result,key=lambda row:(row[3],row[0]))
def build_index(data):
    """Index every occurrence directly to avoid rescanning a train's stops."""
    index={}
    for train,info in data.items():
        for station,arr,dep in info['stops']:index.setdefault(station,[]).append((train,arr,dep))
    return index
def indexed(data,index,station,day):
    """Filter only stop occurrences at the queried station, then sort."""
    matches=[(train,data[train]['name'],arr,dep) for train,arr,dep in index.get(station,[]) if day in data[train]['days']]
    return sorted(matches,key=lambda row:(row[3],row[0]))
def flat_scan(rows,station,day):
    """Flat-list alternative with the same query output."""
    result=[(train,name,arr,dep) for train,name,stop,arr,dep,days in rows if stop==station and day in days]
    return sorted(result,key=lambda row:(row[3],row[0]))
def generated(n):
    """Build n trains with ten unique stations per train and zero-padded times."""
    result={}
    for i in range(n):
        stops=[]
        for j in range(10):
            minute=360+j*45+i%30
            stops.append((f'S{(i+j)%100:03d}',f'{minute//60:02d}:{minute%60:02d}',f'{(minute+5)//60:02d}:{(minute+5)%60:02d}'))
        result[f'T{i:05d}']=dict(name=f'Train {i}',stops=stops,days={'Mon','Wed','Fri'} if i%2 else set(DAYS))
    return result
if __name__=='__main__':
    data=fixture();index=build_index(data)
    expected=['T104','T102','T101']
    actual=scan(data,'Central','Mon');assert [r[0] for r in actual]==expected
    assert actual==indexed(data,index,'Central','Mon')
    assert scan(data,'Unknown','Mon')==[]==indexed(data,index,'Unknown','Mon')
    assert all(row[0]!='T103' for row in actual)
    print('Fictional timetable: Central on Monday')
    for train,name,arrival,departure in actual:print(f'{train:<7}{name:<18}{arrival:>7}{departure:>7}')
    print('Third stop departure:',data['T101']['stops'][2][2])
    print('Unknown station and non-running-day checks PASS')
    results=[]
    for n in [100,1000,10000]:
        data=generated(n);begin=perf_counter();index=build_index(data);build_time=perf_counter()-begin
        flat=[(train,info['name'],station,arr,dep,info['days']) for train,info in data.items() for station,arr,dep in info['stops']]
        row={'trains':n,'total_stops':n*10,'station_candidates':len(index.get('S005',[])),'queries':20,'index_build_seconds':build_time}
        outputs=[]
        for name,fn in [('scan',lambda:scan(data,'S005','Mon')),('indexed',lambda:indexed(data,index,'S005','Mon')),('flat',lambda:flat_scan(flat,'S005','Mon'))]:
            begin=perf_counter()
            for _ in range(20):answer=fn()
            row[name+'_seconds']=(perf_counter()-begin)/20;outputs.append(answer)
        assert outputs[0]==outputs[1]==outputs[2]
        # Count newly allocated container overhead, excluding referenced strings/base data.
        row['index_container_bytes']=sys.getsizeof(index)+sum(sys.getsizeof(v)+sum(sys.getsizeof(t) for t in v) for v in index.values())
        results.append(row)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

"""Attempt the quadratic 100000-record alternative with a three-second watchdog."""
import subprocess,sys,tempfile,json
from pathlib import Path
from time import perf_counter
if __name__=='__main__':
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'progress.json';begin=perf_counter()
        try:
            run=subprocess.run([sys.executable,str(Path(__file__).with_name('pairwise_trial.py')),str(path)],capture_output=True,text=True,timeout=3,check=True)
            result={'status':'COMPLETED','result':json.loads(run.stdout)}
        except subprocess.TimeoutExpired:
            result={'status':'TIMEOUT_3_SECONDS','parent_elapsed_seconds':perf_counter()-begin,
                    'progress_checkpoint':json.loads(path.read_text()) if path.exists() else None,
                    'required_pairs':4999950000,'note':'No full-run completion time is claimed.'}
    Path(__file__).with_name('large_trial.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

"""Run all CO3 experiments and preserve genuine output and execution metadata."""
from pathlib import Path
import subprocess,sys,json

ROOT=Path(__file__).resolve().parents[1]
JOBS={'Q1':['rainfall.py'],'Q2':['complete_code.py','copying.py'],
      'Q3':['complete_code.py','complaints.py'],'Q4':['complete_code.py','electives.py'],
      'Q5':['sensors.py'],'Q6':['timetable.py'],
      'Q7':['contacts.py','large_comparison.py']}

def main():
    """Run every example with assertions enabled; stop if any program fails."""
    results=[]
    for folder,files in JOBS.items():
        output=[]
        for file in files:
            command=f'{folder}/{file}'
            run=subprocess.run([sys.executable,command],cwd=ROOT,text=True,
                               capture_output=True,check=True,timeout=90)
            output.append(f'$ python3 {command}\n'+run.stdout)
            if run.stderr:output.append('STDERR:\n'+run.stderr)
            results.append({'program':command,'exit_code':run.returncode})
        (ROOT/folder/'output.txt').write_text('\n'.join(output))
        print(folder,'PASS',flush=True)
    (ROOT/'verification.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
    print('All programs passed. The intentionally bounded Q7 trial may report TIMEOUT_3_SECONDS.')

if __name__=='__main__':main()

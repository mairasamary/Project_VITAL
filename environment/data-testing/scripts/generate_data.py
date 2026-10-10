#!/usr/bin/env python3
"""Project VITAL A4 deterministic synthetic dataset generator (CSV schema v1)."""
import argparse
import csv
import hashlib
import json
import random
from datetime import date, timedelta
from pathlib import Path

LEVELS = {'small': 200, 'medium': 2000, 'large': 20000}
FIELDS = {
 'patients': ['pid','pubpid','fname','lname','DOB','sex','city','state'],
 'encounters': ['encounter','pid','date','reason'],
 'appointments': ['appointment_id','pc_pid','pc_eventDate','pc_startTime','pc_endTime','pc_duration','pc_catid','pc_apptstatus'],
 'vitals': ['vital_id','pid','encounter','date','bps','bpd','pulse','weight','height'],
}

def generate(level, seed, output):
    rng = random.Random(seed)
    output.mkdir(parents=True, exist_ok=True)
    handles = {}
    writers = {}
    counts = {name: 0 for name in FIELDS}
    try:
        for name, fields in FIELDS.items():
            handles[name] = (output / f'{name}.csv').open('w', newline='', encoding='utf-8')
            writers[name] = csv.DictWriter(handles[name], fieldnames=fields, lineterminator='\n')
            writers[name].writeheader()
        encounter_id = vital_id = appointment_id = 0
        for pid in range(1, LEVELS[level] + 1):
            dob = date(1940, 1, 1) + timedelta(days=rng.randrange(27000))
            writers['patients'].writerow({'pid':pid,'pubpid':f'VITAL-{pid:07d}', 'fname':f'Synthetic{pid}', 'lname':'Testpatient', 'DOB':dob.isoformat(), 'sex':rng.choice(['Male','Female']), 'city':'Testville', 'state':'MA'})
            counts['patients'] += 1
            for _ in range(rng.randrange(0, 4)):
                encounter_id += 1
                day = date(2025, 1, 1) + timedelta(days=rng.randrange(365))
                stamp = f'{day.isoformat()} 09:00:00'
                writers['encounters'].writerow({'encounter':encounter_id,'pid':pid,'date':stamp,'reason':'Synthetic testing encounter'})
                counts['encounters'] += 1
                if rng.random() < 0.8:
                    vital_id += 1
                    writers['vitals'].writerow({'vital_id':vital_id,'pid':pid,'encounter':encounter_id,'date':stamp,'bps':(bps := rng.randrange(95,151)),'bpd':rng.randrange(60,min(96,bps)),'pulse':rng.randrange(55,106),'weight':round(rng.uniform(45,110)*2.2046226218,2),'height':round(rng.uniform(145,195)/2.54,2)})
                    counts['vitals'] += 1
            for _ in range(rng.randrange(0, 3)):
                appointment_id += 1
                day = date(2026, 1, 1) + timedelta(days=rng.randrange(365))
                hour = rng.randrange(8, 17)
                writers['appointments'].writerow({'appointment_id':appointment_id,'pc_pid':str(pid),'pc_eventDate':day.isoformat(),'pc_startTime':f'{hour:02d}:00:00','pc_endTime':f'{hour:02d}:30:00','pc_duration':1800,'pc_catid':5,'pc_apptstatus':'-'})
                counts['appointments'] += 1
    finally:
        for handle in handles.values():
            handle.close()
    hashes = {name:hashlib.sha256((output/f'{name}.csv').read_bytes()).hexdigest() for name in FIELDS}
    metadata = {'schema_version':1,'generator_version':'0.1.2','level':level,'seed':seed,'counts':counts,'sha256':hashes,'note':'Synthetic CSV fixture IDs are not database primary keys; loader must map identifiers and create forms registry entries.'}
    (output/'metadata.json').write_text(json.dumps(metadata, indent=2, sort_keys=True)+'\n',encoding='utf-8')
    return metadata

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--level',choices=LEVELS,required=True)
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(generate(args.level,args.seed,args.output),indent=2))

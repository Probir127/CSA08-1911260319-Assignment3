"""Bounded every-pair 100000-contact trial; progress is never fabricated."""
from contacts import generated,pairwise
from pathlib import Path
from time import perf_counter
import sys,json
progress=Path(sys.argv[1]);records=generated(100000);begin=perf_counter()
def save(count):
    """Save actual progress periodically, outside any inference about completion."""
    progress.write_text(json.dumps({'completed_pair_comparisons':count,'worker_elapsed_seconds':perf_counter()-begin}))
answer,count=pairwise(records,save)
print(json.dumps({'groups':len(answer),'comparisons':count,'seconds':perf_counter()-begin}))

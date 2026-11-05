# CSA08 - Assignment 3 (CO3)

Student Name: PROBIR SAHA SHOHOM  
Register Number: 1911260319  
Course: CSA08 - Python Programming  
Repository: https://github.com/Probir127/CSA08-1911260319-Assignment3

[PDF report](CSA08_Assignment3_Solution.pdf) | [Text report](SOLUTIONS.md)

Python 3.10+; standard library only. The exact execution version is in verification.json.
No third-party runtime requirements are needed.

## Run every question

```text
python3 tools/run_all.py
```

Do not use -O: it disables assertions. The runner captures output.txt, measurements.json and verification.json. The deliberately bounded Q7 every-pair trial may record TIMEOUT_3_SECONDS, which is a disclosed scalability outcome, not a claimed completed time. Figures and report tables correspond to the captured preparation run; re-running changes timings.

## Commands and results

| Question | Commands | Result |
|---|---|---|
| Q1 | `python3 Q1/rainfall.py` | Weekly/dry-day reports; naive, running and deque averages agree; 3 sizes timed |
| Q2 | `python3 Q2/complete_code.py`; `python3 Q2/copying.py` | Aliasing repaired; identity/copy tests pass; 1,000,000-value memory/timings measured |
| Q3 | `python3 Q3/complete_code.py`; `python3 Q3/complaints.py` | Expected top words; normalized/grouped records; 4 counters agree at 3 sizes |
| Q4 | `python3 Q4/complete_code.py`; `python3 Q4/electives.py` | Expected clash/exactly-one/neither reports; methods agree; membership and intersections measured |
| Q5 | `python3 Q5/sensors.py` | Three complete cleaning reports agree; boundary/empty tests pass; 3 sizes and generator memory measured |
| Q6 | `python3 Q6/timetable.py` | Five fictional trains; station/day tests pass; index/scan/flat outputs match at 3 sizes |
| Q7 | `python3 Q7/contacts.py`; `python3 Q7/large_comparison.py` | Hand/bridge/missing-field tests pass; dictionary merge finishes 100,000 contacts; pairwise large trial bounded |

Synthetic input generators are embedded in the source. Q1/year_summary.json retains all annual weekly totals and dry days. Q7/sample_input.json and sample_output.json retain the hand-worked contact fixture. All contacts and railway services are fictional examples.

## Evidence and submission

Prepared with Codex assistance. Output images are labelled renderings of actual captured stdout, not terminal screenshots. Capture any faculty-required terminal screenshots when personally running the code. Raw operation counts, timings and shallow memory measurements are included and explained in the report. Commits record this preparation session and are not backdated to imply a week of development. Review the solution and submit the repository URL to the faculty; no faculty invitation or final course submission has been made.

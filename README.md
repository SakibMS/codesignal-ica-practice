# CodeSignal ICA practice

Five practice tasks in the format of CodeSignal's Industry Coding Assessment (the "filesystem + unit tests" one): implement one class across **4 progressive levels**, graded by unit tests.

| # | Module | Levels |
|---|---|---|
| 1 | `01_inventory`: inventory manager | stock → reports → expiring reservations → price changes + revenue history |
| 2 | `02_database`: in-memory database | records → scans → TTL → backup / restore |
| 3 | `03_cloud_storage`: cloud storage | files → search → user quotas → file versions |
| 4 | `04_banking`: banking system | accounts → top spenders → scheduled payments → merges + balance history |
| 5 | `05_payroll`: payroll | clock in/out → rankings → pay rates → bonus periods |

Roughly easiest to hardest. All problems are original.

## Setup

Python 3.8+. No packages needed.

```
git clone https://github.com/SakibMS/codesignal-ica-practice.git
cd codesignal-ica-practice
```

## How to practise

1. Set a 90-minute timer (about 10 / 20 / 30 / 30 minutes per level).
2. Read `01_inventory/spec/level1.md` and implement it in `01_inventory/inventory.py`.
3. Run `python3 run.py 1 --level 1`.
4. When a level passes, open the next spec and add its methods. `--level N` runs levels 1 to N, so you also catch regressions.
5. Don't read ahead. In the real test the next level unlocks only after you finish the current one, and it may force a refactor.
6. Afterwards, compare with `solutions/`.

```
python3 run.py 1                # all levels of module 1
python3 run.py 1 --solution     # run the reference solution
python3 run.py all --solution   # score summary for every module
```

On Windows, use `python` instead of `python3`. To retry a module, reset your file with `git checkout -- 01_inventory/inventory.py` (or use a branch per attempt).

## Layout (mirrors CodeSignal)

```
01_inventory/
  inventory.py          your code (starts with level 1 methods only)
  spec/level1..4.md     the task, one level per file
  tests/basicTests.py   playground: add your own tests (not scored)
  tests/levelNTests.py  graded tests (don't edit)
solutions/              reference solutions
support/                stand-in for the timeout-decorator package CodeSignal uses
run.py                  test runner with a per-level score
```

## Tips

- Match return values exactly: `None` vs `False` vs `0` vs `[]`.
- Match output formats and tie-breaks exactly, e.g. `"id(value)"` sorted by value desc, then id asc.
- Use one dict per entity (`id -> record`) and small helper methods. Later levels add fields.
- For time-based rules, process due events at the start of every method (e.g. `self._process(timestamp)`).
- Level 4 usually asks about the past, so keep raw events or snapshots, not just totals.
- If level 4 stalls, make sure levels 1–3 fully pass. They still count.

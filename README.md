# libpmp: Risk-based project management toolkit

This is the repository for an open-source re-implementation of the
awesomely successful libpmp risk-based estimation and project tracking
software used by Jaybridge Robotics from 2013 to 2016.

## Notes for Users

* This project is not really baked enough for users other than its developers
  right now.  Sorry!

## Developer Setup Notes

* This project is structured as a python wheel build.
* For building and testing, prefer to use a virtual environment:

```bash
python3 -m venv .test_venv
.test_venv/bin/python3 -m pip install --upgrade pip
.test_venv/bin/pip install -e .
```

Of course you can use other environment managers like `uv` or `poetry`; those
are not documented here in order to keep this documentation minimal; `venv`
and `pip` are relatively stable and universal if not actually optimal.

* To perform linter checks run:

```bash
.test_venv/bin/ruff check .
```

* To run all of the tests:

```bash
.test_venv/bin/py.test
```

* To run the `cost` or `progress` estimator scripts, run

```bash
.test_venv/bin/cost
```

or

```bash
.test_venv/bin/progress
```

## Notes for Contributors

* You cannot commit until I (ggould256) add you as a contributor.
* Your first commit must add your name to the [`AUTHORS` file](AUTHORS).
* Please run the checks listed above.

## Design Principles

* Separate subdirectories for time tracking, distribution math,
* Top-level directory should contain the executable scripts.
  docs, progress/leaderboard, emacs fu, etc.
* Time tracking should be via some sort of abstract interface, as
  it is unlikely any two users will have the same time tracking
  conventions.
* Use python3, not python2, primarily because this gets us the
  new division semantics and removes numerical landmines.
* The :closed: RST role in the original libpmp was done as a way to abuse a
  custom role present in trac.  We will not reimplement it; until we
  see otherwise, we will assume that it is sufficient for people to delete
  the estimates from completed tasks.

# libpmp: Risk-based project management toolkit

This is the repository for an open-source reimplementation of the
awesomely successful libpmp risk-based estimation and project tracking
software used by Jaybridge Robotics from 2013 to 2016.

Notes for Users:

 * This project is not really baked enough for users other than its developers
   right now.  Sorry!

Developer Setup Notes:

 * You will need the packages named in `python_requirements.txt` to be
   installed.  There are two ways to do this:
   * You can just `pip3 install -r python_requirements.txt`
   * You can set up a virtual environment.  See `HOWTO.virtualenv` for
     the procedure.
 * Once you have done this, run `make`.  If it succeeds, you are probably
   good to go.

Notes for Contributors:

 * You cannot commit until I (ggould256) add you as a contributor.
 * Your first commit must add your name to the [`AUTHORS` file](AUTHORS).
 * Please ensure that `make` passes before committing.  This checks that:
   * You are up to date with `python_requirements.txt`,
   * Unit tests pass
   * pep8 and pylint pass.
 * Use of virtualenv is at author's discretion but please keep
   `python_requirements.txt` up to date for those who do use it.
   * In addition, future testing infrastructure may use virtualenv.
   * [Notes on getting started with virtual environments](HOWTO.virtualenv.md)

Design Principles:

 * Top-level directory should contain the executable scripts.
 * Separate subdirectories for time tracking, distribution math,
   docs, progress/leaderboard, emacs fu, etc.
 * Time tracking should be via some sort of abstract interface, as
   it is unlikely any two users will have the same time tracking
   conventions.
 * Use python3, not python2, primarily because this gets us the
   new division semantics and removes numerical landmines.
 * The :closed: RST role in the original libpmp was done as a way to abuse a
   custom role present in trac.  We will not reimplement it; unti we
   see otherwise, we will assume that it is sufficient for people to delete
   the estimates from completed tasks.

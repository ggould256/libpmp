# libpmp: Risk-based project management toolkit

This is the repository for an open-source reimplementation of the
awesomely successful libpmp risk-based estimation and project tracking
software used by Jaybridge Robotics from 2013 to 2016.

Notes for Contributors:

 * Top-level directory should contain the executable scripts.
 * Separate subdirectories for time tracking, distribution math,
   docs, progress/leaderboard, emacs fu, etc.
 * Time tracking should be via some sort of abstract interface, as
   it is unlikely any two users will have the same time tracking
   conventions.
 * Use python3, not python2, primarily because this gets us the
   new division semantics and removes numerical landmines.
 * Use of virtualenv is at author's discretion but please take care to
   keep python_requirements.txt up to date for those who do use it.
   * In addition, future testing infrastructure may use virtualenv.
 * The :closed: RST role in the original libpmp was done as a way to abuse a
   custom role present in trac.  We will not reimplement it; unti we
   see otherwise, we will assume that it is sufficient for people to delete
   the estimates from completed tasks.

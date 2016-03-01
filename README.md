# libpmp: Risk-based project management toolkit

This is the repository for an open-source reimplementation of the
awesomely successful libpmp risk-based estimation and project tracking
software used by Jaybridge Robotics from 2013 to 2016.

Organization:

 * Top-level directory should contain the executable scripts.
 * Separate subdirectories for time tracking, distribution math,
   docs, progress/leaderboard, emacs fu, etc.
 * Time tracking should be via some sort of abstract interface, as
   it is unlikely any two users will have the same time tracking
   conventions.

Tentative:

 * Default to Python3 rather than python 2 of original?
 * Use virtualenv for unit tests to ensure dependency handling is right?

Open questions:

 * The :closed: RST role in the original libpmp was done as a way to abuse a
   custom role present in trac.  Does this still make sense?  Is more needed?

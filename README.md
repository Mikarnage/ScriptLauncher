# What's this?

A simple python script to schedule script launching.

It's very basic, all it does is:
- Keeps track of the last time the script was launch (thus is restartable).
- Write stdout and stderr to a log file.

It only depends on python, and doesn't need admin rights to run.

# How to use it?

Edit *conf.cfg* with the configuration of the scripts you want to run (the example provided should be self explanatory).

Then run it with `python scriptLauncher.py`.

The last launched date is stored in *conf.cfg*.
Logs are written in the subdirectory *logs*.

# What's the license?

My code is public domain.
It includes the library croniter which is MIT licensed (website here: https://github.com/kiorky/croniter)

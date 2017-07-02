Setting up a Virtual Environment
================================


# Ubuntu example

On ubuntu, the following commands will get you going quickly:

```
  sudo apt-get install python3-dev libblas-dev liblapack-dev gfortran
  virtualenv -p /usr/bin/python-3.4 env
  env/bin/pip install -r python_requirements.txt
  env PATH=env/bin:$PATH make
```


## virtualenvwrapper instructions

If you are used to virtualenvwrapper and are NOT using a mac:
```
  pip3 install virtualenvwrapper
  mkvirtualenv --python=/usr/bin/python3 libpmp
  pip3 install -r python_requirements.txt
```
From this point out you can use `workon libpmp` to enter the virtual
environment and `deactivate libpmp` to leave it.


## mac instructions

If you ARE using a mac, matplotlib is incompatible with standard virtualenv
and you must use python3's spiffy new lightweight `venv` instead.  Or you may
just prefer to use this feature even not on mac!  The commands below will set
up a venv in your `env` directory, which is already gitignored.
```
  python3 -m venv env
  . ./env/bin/activate
  pip3 install -r python_requirements.txt
```
From this point you can source the activate or deactivate scripts to do the
needful via `. ./env/bin/activate` or `deactivate`.


# Ubuntu example

```
sudo apt-get install python3-dev libblas-dev liblapack-dev gfortran
virtualenv -p /usr/bin/python-3.4 env
env/bin/pip install -r python_requirements.txt
env PATH=env/bin:$PATH make
```

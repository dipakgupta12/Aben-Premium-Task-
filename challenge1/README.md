## Setup Chalange 1
## Installation

_Check python3 version using python --version or python3 --version.Make sure python3.8 is installed in system pre commit checks python3.8 and create virtual environment for python3.8_

_follow link for python installation_
for [windows](https://www.python.org/downloads/)
for [linux or mac](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/)

follow link for installtion and creation of virtual environment
[linux or mac](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)
[windows](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
_create virtual environment_

```
virtualenv env
```

Make sure project and virtual environment should be on same level

_Activate environment_

```
source env/bin/activate
```

_Now change directory to project_

```
cd <project_folder_name>
```
_Before installing packages make sure your pip is up to date install it by_ or [follow this link](https://pip.pypa.io/en/stable/installing/)
```
pip install --upgrade pip
```
_Time to install dependencies (It will take a while)_
```
pip install -r requirements.txt
```

### For String Compression Test

```
pytest test_string_compression.py -v
```

### For Network Falure Point Test

```
pytest test_network_failure_point.py -v
```

- This command will start the invoking pytest files
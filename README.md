# feedback-service

## Setting up
0. Install python3
1. Create [virtual environment](https://docs.python.org/3/library/venv.html)
```
python3 -m venv venv
```
2. Activate virtual environment
```
. venv/bin/activate
```
3. Install requirements
```
pip3 install -r requirements.txt
```
4. Migrate
```
python3 manage.py migrate
```
5. Run
```
python3 manage.py runserver
```

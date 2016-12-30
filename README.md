# AWS-Instance-Query

(Optional but recommended) Create a virtual environment using the instructions provided here http://docs.python-guide.org/en/latest/dev/virtualenvs/

## Installation and Setup
Run
```
pip install -r requirements.txt
```
to install dependencies.

You will need your environment variables set for AWS CLI use:
```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```
Run the mongo server using the command appropriate to your operating system from port localhost: port 27017 (mongod)

Run the server using 
```
python app.py
```
to start hosting at localhost:5000

# AWS Lambda Jobs Handler

## Tutorial for running a job

-Open a terminal in the git repository

-Run the command:

`flask run`

-Under the git directory run:

`python3 runjob.py <user_id> <filename>`

Note: file to be tested has to be on the same directory as the _runjob.py_ file

## Checking job status

### Checking all jobs
Open a browser and access the url:
_http://127.0.0.1:5000/_ or _http://127.0.0.1:5000/jobs_

### Checking a specific job
Open a browser and access the url:
_http://127.0.0.1:5000/jobs/<job_id>_

### Checking a specific user's jobs
Open a browser and access the url:
_http://127.0.0.1:5000/users/<user_id>_

## Changing test file and it's input
-Change your test file as you want:

#### Example:
test file:

```
def main():
    i = 0
    while(i < 10000000):
        i += 1
    return arg1+arg2
print(main())
```

-Open the _runjob.py_ and edit the parameters variable:

`parameters = {'arg1': 1, 'arg2': 2}`


Make sure that your paramenter have the same name as in the _parameters_ variable under the _runjob.py_ file.
In this example _arg1_ and _arg2_ will be substituted for the values _1_ and _2_ respectively. What happens is that the python test file will no longer see the values as _arg1_ and _arg2_ but as _1_ and _2_.

__Note: the return value of the function in the python test file needs to be _printed_, as the lambda handler will capture the value that is printed__

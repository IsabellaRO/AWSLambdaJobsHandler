# AWS Lambda Jobs Handler

## Tutorial for running a job

-Open a terminal in the git repository

-Run the command:

`flask run`

-Under the git directory run:

`python3 runjob.py <user_id> <filename>`

Note: file has to be on the same directory as the runjob.py file

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
-Change your file's variables as they were defines:

test file:

`def main():
    i = 0
    while(i < 10000000):
        i += 1
    return arg1+arg2
print(main())`

-Open the _runjob.py_ and edit the parameters variable:

`
'''

    Function parameters (ex: {'a': 1, 'b': 2})
    '''
    
    parameters = {'arg1': 1, 'arg2': 2}`


In this example arg1 and arg2 will be substituted for 

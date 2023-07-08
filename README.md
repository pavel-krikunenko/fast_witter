## simple RESTful API using FastAPI for a social networking application

### Requirements

<p>all requirements in file requirements.txt on project root directory. </p>
install requirements command:
``` python3 -m pip install -r requirements.txt ```

### Config

<p>default project config path = {project_root}/etc/config.json </p>
#### config required_fields:
- debug:bool
- salt: string , this field need for encrypt user password
- db:dsn: string , it is DB url
- redis:dsn strin, redis url

### Migrations

<p>
for migrations use service [dbmate](https://github.com/amacneil/dbmate) .
migrations directory {project_root}/etc/migrations
</p>

### RUN

default server run on 8010 port

- #### Docker
    - ``` docker-compose build ```
    - ``` docker-compose up ```
    - or
    - ``` docker-compose up --build ```

### TESTS

after run project in docker

- ```docker run ftwitter pytest tests ``` run all tests
- ```docker run ftwitter pytest tests/api/test_auth.py``` run tests for one module
- ```docker run ftwitter pytest tests/api/test_auth.py::test_auth_me``` run one test

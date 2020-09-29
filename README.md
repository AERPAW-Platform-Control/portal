# AERPAW Portal

**THIS IS A WORK IN PROGRESS**

Initial development framework for AERPAW Portal

- Web framework ([Django](https://docs.djangoproject.com/en/3.1/))
- Web server gateway interface ([uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/))
- Web server / reverse proxy ([Nginx](https://hub.docker.com/_/nginx/))
- Database ([PostgreSQL](https://www.postgresql.org/docs/12/index.html))
- OIDC Authentication ([CILogon](https://www.cilogon.org/oidc))
- OpenSSL development certificates ([OpenSSL](https://www.openssl.org))

## Table of Contents

- [Setting up your Development Environment](#setup)
- [Running the Development Environment](#run-dev)
- [Running everything in Docker](#run-in-docker)
- [Cleaning it all up](#cleanup)
- [User model](#user-model)

## <a name="setup"></a>Setting up your Development Environment

Requirements

- Python 3 (with Pip 3 and virtualenv)
- Docker
- Docker Compose

The AERPAW Portal is a Django based application, and the code itself should be run on your local machine for development. My preferred Python virtual environment is [virtualenv](https://virtualenv.pypa.io/en/latest/), so the documentation herein will make use of it.

## <a name="run-dev"></a>Running the Development Environment

### Configuration

Some configuration is required prior to running the development environment.

- copy the `en.template` file as `.env`
    - populate the `.env` file with values for `OIDC_RP_CLIENT_ID` and `OIDC_RP_CLIENT_SECRET` (all other values should have sane defaults, but may need to be adjusted based on your local setup)

### Docker containers

The `docker-compose.yml` file at the top level of the repository is meant for development use. Other compose definitions can be found in the `compose` directory.

```
docker-compose pull
docker-compuse up -d
```

Verify that the containers are running as expected. You should observe two running containers.

```
$ docker-compose ps
    Name                  Command               State                      Ports
---------------------------------------------------------------------------------------------------
;      docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
aerpaw-nginx   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:8443->443/tcp, 0.0.0.0:8080->80/tcp
```

And the database should be ready to accept connections.

```
$ docker-compose logs database
Attaching to aerpaw-db
...
aerpaw-db   | PostgreSQL init process complete; ready for start up.
aerpaw-db   |
aerpaw-db   | 2020-09-29 16:09:17.018 UTC [1] LOG:  starting PostgreSQL 12.4 (Debian 12.4-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
aerpaw-db   | 2020-09-29 16:09:17.019 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
aerpaw-db   | 2020-09-29 16:09:17.019 UTC [1] LOG:  listening on IPv6 address "::", port 5432
aerpaw-db   | 2020-09-29 16:09:17.021 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
aerpaw-db   | 2020-09-29 16:09:17.080 UTC [57] LOG:  database system was shut down at 2020-09-29 16:09:16 UTC
aerpaw-db   | 2020-09-29 16:09:17.104 UTC [1] LOG:  database system is ready to accept connections
```

### Django

Create a virtual environment at the top level of the repository, activate it, and pip install the requirements file

```console
virtualenv -p $PATH_TO_PYTHON3 venv
source venv/bin/activate
pip install -r requirements.txt
```

Once completed you should now be ready to run the script that launches the Django applicaiton using uWSGI

```console
UWSGI_UID=$(id -u) UWSGI_GID=$(id -g) ./run_uwsgi.sh
```

Navigate to [https://127.0.0.1:8443/](https://127.0.0.1:8443/) in your browser (may encounter a security warning due to using a self signed certificate) and you should observe the following:

![](docs/images/home.png)

Follow the [Log In]() link to the `login.html` page, and proceed to CILogon

![](docs/images/cilogon.png)

Choose your identity provider from the dropdown and authenticate. Upon successful authentication you should see a page populated with your CILogon Claims as provided by your identity provider.

![](docs/images/authenticated.png)

## <a name="run-in-docker"></a>Running everything in Docker

### Configuration

Some configuration is required prior to running the production environment.

- copy the `env.template` file as `.env`
    - populate the `.env` file with values for `OIDC_RP_CLIENT_ID` and `OIDC_RP_CLIENT_SECRET` (all other values should have sane defaults, but may need to be adjusted based on your local setup)
    - update value `export POSTGRES_HOST=database`
- copy the `nginx/production.conf` file as `nginx/default.conf`
- in the `uwsgi.ini` file

    ```
    [uwsgi]
    ...
    # use for development
    ;socket = :8000
    
    # use for production
    uwsgi-socket = ./base.sock
    chmod-socket = 666
    ```
 

### Docker containers

Copy the `compose/production-compose.yml` file as `docker-compose.yml`

```
docker-compose pull
docker-compose build
UWSGI_UID=$(id -u) UWSGI_GID=$(id -g) docker-compose up -d
```

Verify that the containers are running as expected. You should observe three running containers (only ports 8080 and 8443 are exposed to the outside, all other connections occur on a local subnet).

```
$ docker-compose ps
    Name                   Command               State                      Ports
----------------------------------------------------------------------------------------------------
aerpaw-db       docker-entrypoint.sh postgres    Up      5432/tcp
aerpaw-nginx    /docker-entrypoint.sh ngin ...   Up      0.0.0.0:8443->443/tcp, 0.0.0.0:8080->80/tcp
aerpaw-portal   /code/docker-entrypoint.sh       Up
```

Once the django container completes building it should present something similar to

```
$ docker-compose logs django
Attaching to aerpaw-portal
...
aerpaw-portal | mapped 145840 bytes (142 KB) for 1 cores
aerpaw-portal | *** Operational MODE: single process ***
aerpaw-portal | WSGI app 0 (mountpoint='') ready in 3 seconds on interpreter 0x5632c13d44b0 pid: 668 (default app)
aerpaw-portal | *** uWSGI is running in multiple interpreter mode ***
aerpaw-portal | spawned uWSGI master process (pid: 668)
aerpaw-portal | spawned uWSGI worker 1 (pid: 670, cores: 1)
```

Navigate to [https://127.0.0.1:8443/](https://127.0.0.1:8443/) in your browser (may encounter a security warning due to using a self signed certificate) and you should observe the following:

![](docs/images/home.png)

## <a name="cleanup"></a>Cleaning it all up

### Docker

Use `docker-compose` to stop and remove your containers when finished

```
docker-compose stop
docker-compose rm -fv
```

### Django

The locally running Django application can be terminated by issuing a `ctrl-c` in the terminal it is running in (unless you've backgrounded the process in which case you'll need to terminate it by PID instead)

```console
# find the process associated with the bash ./run_uwsgi.sh call
$ ps -a
  PID TTY           TIME CMD
...
41712 ttys000    0:00.01 bash ./run_uwsgi.sh
41725 ttys000    0:00.28 uwsgi --uid 503 --gid 20 --virtualenv ./venv --ini uwsgi.ini
41727 ttys000    0:00.33 uwsgi --uid 503 --gid 20 --virtualenv ./venv --ini uwsgi.ini
...
41841 ttys001    0:00.00 ps -a

# terminate it along with the uswgi processes it spawned
$ kill -9 41712 41725 41727
```

### Directories

Some directories are created and populated during the running of the application. These can be left in tact on your local system, or removed prior to the next restart of the application if you do not wish to persist prior data.

- `pg_data/` - contents of the database and shared with the Docker database container
- `accounts/migrations/` - generated database migrations that map the Python objects to the database tables (as more Django apps are added, more migrations directories will begin to appear)
- `static/` and `media/` - the contents of these directories depend on the css, js, and additional static artifacts required to run the site and are expected to evolve over time

## <a name="user-model"></a>User model

The `AerpawUser` custom user model extends the base user model with OIDC Claims discovered on login. 

Base User objects have the following fields:

- **username** - Required. 150 characters or fewer. Usernames may contain alphanumeric, `_`, `@`, `+`, `.` and `-` characters
- **first\_name** - Optional (`blank=True`). 150 characters or fewer
- **last\_name** - Optional (`blank=True`). 150 characters or fewer
- **email** - Optional (`blank=True`). Email address
- **password** - Required. A hash of, and metadata about, the password
- **groups** - Many-to-many relationship to Group
- **user\_permissions** - Many-to-many relationship to Permission
- **is\_staff** - Boolean. Designates whether this user can access the admin site
- **is\_active** - Boolean. Designates whether this user account should be considered active
- **is\_superuser** - Boolean. Designates that this user has all permissions without explicitly assigning them
- **last\_login** - A datetime of the user’s last login
- **date\_joined** - A datetime designating when the account was created

Ref: [https://docs.djangoproject.com/en/3.1/ref/contrib/auth/](https://docs.djangoproject.com/en/3.1/ref/contrib/auth/)

     

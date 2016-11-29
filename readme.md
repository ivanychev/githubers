# Building Github graph

The project is aimed at building graph of GitHub users. The code is written in Python 3.

At the moment there are two scripts, that are contained id `/src` folder.

*   `download_users.py` – scripts must be launched with two following arguments: GitHub login and password of registered user. For example:

```bash
python3 main.py Vasya crocodile3
```
`download_users.py` downloads GitHub users information and stores it to SQLite database.
During launch, the script scans the `path` for the DB, finds maximal downloaded id and starts requesting for greater ones, so the program can be stopped and continued at any time.

*   `githubers.py` – utilities, which `main.py` is using.

*   `config.py` – module loads configuration file and sets parameters according to `/resourses/config.json` file. Relative `path`, where loaded jsons are stored, is contained here.

## Launching

Launch `download_users.py` following your Github login and password. See `download_users.py` docstring for extra example.

## Requirements

*   You need `sqlite3` to be installed on your machine.
*   Python 3 (+ `toolz`, `requests` packages)

## TODO

-   [ ] Download following/followers information
-   [ ] Download organisations information

## Note

The folder with DB **must** exist, if you make a fresh start. 

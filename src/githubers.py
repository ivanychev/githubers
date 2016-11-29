from os.path import isfile
import requests
from toolz import *
from toolz.curried import *
import sqlite3
from collections import namedtuple

USER_FIELDS = ("UserID", "Login", "Type", "Created_at", "OrganisationsURL", "FollowingURL", "UserURL")
USER_FIELDS_JSON = ("id", "login", "type", "organizations_url", 'subscriptions_url', 'url')
USER_FACTORY = namedtuple("User_repr", USER_FIELDS)
USERS_INIT_COMMAND = """create table Users
(
   {} integer primary key,
   {} text not null,
   {} text not null,
   {} text,
   {} text,
   {} text,
   {} text
)
""".format(*USER_FIELDS)
FOLLOWINGS_FIELDS = ("Follower", "Following")
FOLLOWINGS_INIT_COMMAND = """create table Followers
(
  {} integer not null,
  {} integer not null
)
""".format(*FOLLOWINGS_FIELDS)
MEMBERSHIP_FIELDS = ("OrganisationID", "UserID", "PublicityFlag")
MEMBERSHIP_INIT_COMMAND = """create table Membership
(
  {} integer not null,
  {} integer not null,
  {} integer
)
""".format(*MEMBERSHIP_FIELDS)


def compose_named_tuple(raw_tuple):
    raw = list(raw_tuple)
    raw.insert(3, None)
    return USER_FACTORY(*raw)

def remote_users(login, password, since_id=0, per_request=100):
    print("Hello")
    end = False
    if since_id is None:
        since_id = 0
    process = compose(compose_named_tuple, get(list(USER_FIELDS_JSON)))
    while not end:
        req = "".join(["https://api.github.com/users?since=", str(since_id), "&per_page=", str(per_request)])
        response = requests.get(req, auth=(login, password))
        end = len(req) == 0
        if end:
            break
        jsons = response.json()
        since_id = max(map(get("id"), jsons))
        yield from map(process, jsons)


def configure_db(conn):
    c = conn.cursor()
    c.execute(USERS_INIT_COMMAND)
    c.execute(FOLLOWINGS_INIT_COMMAND)
    c.execute(MEMBERSHIP_INIT_COMMAND)


def connect_db(path):
    is_db = isfile(path)
    conn = sqlite3.connect(path)
    if not is_db:
        configure_db(conn)
    return conn


def max_user_id(conn):
    c = conn.cursor()
    c.execute("""select max({})
    from Users""".format(USER_FIELDS[0]))
    return list(c)[0][0]

def add_user(cursor, user_tuple):
    cursor.execute("insert into Users values (?,?,?,?,?,?,?)", user_tuple)


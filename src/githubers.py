"""
Necessary utilities of the project.

Version: 0.1
Author: Sergey Ivanychev
"""

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
    """
    Converts raw tuple to the named one

    :param raw_tuple: tuple that contains user information
    :return: namedtuple
    """
    raw = list(raw_tuple)
    raw.insert(3, None)
    return USER_FACTORY(*raw)

def remote_users(login, password, since_id=0, per_request=100):
    """
    Downloads user information and yields user information as namedtuples.

    :param login: GitHub username
    :param password: GitHub password
    :param since_id: starting id
    :param per_request: how many users to download per each request
    :return: the generator
    """
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
    """
    Creates all necessary tables in the DB.

    :param conn: connection instance of the DB
    :return: None
    """
    c = conn.cursor()
    c.execute(USERS_INIT_COMMAND)
    c.execute(FOLLOWINGS_INIT_COMMAND)
    c.execute(MEMBERSHIP_INIT_COMMAND)


def connect_db(path):
    """
    Connects to existing database or creates new if necessary.

    :param path: path to the DB
    :return: sqlite.connection instance to the DB.
    """
    is_db = isfile(path)
    conn = sqlite3.connect(path)
    if not is_db:
        configure_db(conn)
    return conn


def max_user_id(conn):
    """
    Requests max UserID from the DB.

    :param conn: the DB connection instance
    :return: max id or None, if the Users table is empty
    """
    c = conn.cursor()
    c.execute("""select max({})
    from Users""".format(USER_FIELDS[0]))
    return list(c)[0][0]

def add_user(cursor, user_tuple):
    """
    Adds user to the DB.Users

    :param cursor: cursor of the DB
    :param user_tuple: raw user data
    :return: None
    """
    cursor.execute("insert into Users values (?,?,?,?,?,?,?)", user_tuple)


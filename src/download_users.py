#!/usr/bin/env python3

import sys
import config
import githubers as g
CONFIG_PATH = "../resources/config.json"


def check_args(argv):
    if len(argv) != 3:
        print("Github login and password are expected as script parameters")
        return False
    return True


def main(argv):
    if not check_args(argv):
        return -1
    login, password = argv[1], argv[2]
    db_path = config.read_config(CONFIG_PATH)
    conn = g.connect_db(db_path)
    cursor = conn.cursor()
    max_id = g.max_user_id(conn)
    for user_tuple in g.remote_users(login, password, since_id=max_id):
        g.add_user(cursor, user_tuple)
        conn.commit()
        print("added {}:{}".format(user_tuple.UserID, user_tuple.Login))

if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
import os
import sys
import json
import getpass

from lesspass import lesspass

LESSPASS_PROFILES_DIR='~/.lesspass'

class IncompleteProfile(Exception):
    def __init__(self, field):
        self.field = field

    def get_field(self):
        return self.field

def load_profile(name):
    dir_path = os.path.expanduser(LESSPASS_PROFILES_DIR)
    profile_path = os.path.join(dir_path, "{}.json".format(name))

    with open(profile_path, 'r') as f:
        profile = json.loads(f.read())
        return profile

    return None

def main(site, login, profile = None):
    try:
        user_profile = load_profile(profile) if profile else None
        if site is None and login is None:
            if 'login' not in user_profile:
                raise IncompleteProfile('login')

            if 'site' not in user_profile:
                raise IncompleteProfile('site')

            site = user_profile['site']
            login = user_profile['login']

        password_profile = lesspass._get_password_profile(user_profile)
        master_password = getpass.getpass("LessPass Master Password: ")
        password = lesspass.generate_password(site, login,
                                              master_password, password_profile)
        print(password)
    except KeyboardInterrupt:
        print("Program stopped by user!", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as err:
        print("Profile {} not found!".format(profile), file=sys.stderr)
        sys.exit(1)
    except IncompleteProfile as err:
        msg = "You should set {} in your profile " \
              "file or set it in command line!".format(err.get_field())
        print(msg, file=sys.stderr)
        sys.exit(2)
    except:
        print("An error occurred!", file=sys.stderr)
        sys.exit(1)

def print_login(profile):
    user_profile = load_profile(profile)
    if user_profile is None:
        print("No such profile: {}".format(profile))
        sys.exit(1)

    if 'login' in user_profile:
        print(user_profile['login'])
    else:
        print("There is no 'login' field in configuration: {}".format(profile))
        sys.exit(2)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc == 1 or argc > 5:
        print("Usage: {} [--login] [profile] [website login]".format(sys.argv[0]),
              file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] == "--login" and argc >= 3:
        print_login(sys.argv[2])
    elif argc == 3:
        main(*sys.argv[1:])
    elif argc == 4:
        main(sys.argv[2], sys.argv[3], sys.argv[1])
    else:
        main(None, None, sys.argv[1])


#!/usr/bin/python
# Grabs a list of all satellite users and prints their usernames
import xmlrpclib
import getpass

SATELLITE_URL = "http://rhn.rice.edu/rpc/api"
SATELLITE_LOGIN = "username"
SATELLITE_PASSWORD = "password"


if __name__ == "__main__":
    client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
    SATELLITE_LOGIN = str(raw_input("RHN Userid > ")).rstrip()
    SATELLITE_PASSWORD = getpass.getpass() 

    key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
    list = client.user.list_users(key)
    for user in list:
       print user.get('login')
    client.auth.logout(key)

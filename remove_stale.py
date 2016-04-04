#!/usr/bin/python
# Removes from satellite any profiles not checking in within the last STALE_DAYS days

import xmlrpclib
import getpass
import datetime

SATELLITE_URL = "https://YOUR.SATELLITE.SERVER/rpc/api"
# Uncomment and set values for automated login
#SATELLITE_LOGIN = "userid"
#SATELLITE_PASSWORD = "password"
STALE_DAYS = 90

if __name__ == "__main__":
    client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
    SATELLITE_LOGIN = str(raw_input("RHN Userid: ")).rstrip()
    SATELLITE_PASSWORD = getpass.getpass() 

    key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
    result_array = client.system.listInactiveSystems(key,STALE_DAYS)
    client.system.deleteSystems(key, [profile['id'] for profile in result_array])

    client.auth.logout(key)

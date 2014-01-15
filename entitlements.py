#!/usr/bin/python
# Removes a particular entitlement from all your systems
# Set TARGET_ENTITLEMENT to one of 'enterprise_entitled', 'provisioning_entitled',
# 'monitoring_entitled', 'nonlinux_entitled', 'virtualization_host', or 'virtualization_host_platform'.
import xmlrpclib
import getpass
import datetime

SATELLITE_URL = "http://YOUR.SERVER.HOSTNAME/rpc/api"
SATELLITE_LOGIN = "userid"
SATELLITE_PASSWORD = "password"

TARGET_ENTITLEMENT = ['monitoring_entitled']


if __name__ == "__main__":
    client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
    SATELLITE_LOGIN = str(raw_input("RHN Userid: ")).rstrip()
    SATELLITE_PASSWORD = getpass.getpass() 

    key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
    result_array = client.system.listSystems(key)
    for profile in result_array:
        id = profile['id']
        client.system.removeEntitlements(key, id, TARGET_ENTITLEMENT) 

    client.auth.logout(key)

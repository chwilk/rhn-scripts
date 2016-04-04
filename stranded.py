#!/usr/bin/python
# Generates a list, for the current user's organization, of any machine that has a low
# enough version of redhat-release installed that it cannot be migrated to Red Hat 
# Satellite 6
import xmlrpclib
import getpass
import datetime

# Replace with your satellite here
SATELLITE_URL = "https://YOUR.SATELLITE.SERVER/rpc/api"
#SATELLITE_LOGIN = "userid"
#SATELLITE_PASSWORD = "password"


if __name__ == "__main__":
    client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
    # Comment out below to hardwire userid and pass (not recommended outside of debugging)
    SATELLITE_LOGIN = str(raw_input("RHN Userid: ")).rstrip()
    SATELLITE_PASSWORD = getpass.getpass() 
    # Log in
    key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)

    # Build list of relevant package IDs
    # Apologies for the specific versions entered here.
    # Please double-check against your own installation to ensure this list is sufficient
    # If you use RHEL4 ES instead of AS, or still have RHEL3 or below, you might add that.
    # Syntax for the search strings is documented at: http://lucene.apache.org/core/3_5_0/queryparsersyntax.html
    releases = []
    releases += client.packages.search.advanced(key, 'name:redhat-release AND (version:4AS OR version:4WS)')
    releases += client.packages.search.advanced(key, 'name:redhat-release AND (version:5Server OR version:5Client) AND release:5.0.0.9')
    releases += client.packages.search.advanced(key, 'name:redhat-release AND (version:5Server OR version:5Client) AND release:5.1.0.2')
    releases += client.packages.search.advanced(key, 'name:redhat-release AND (version:5Server OR version:5Client) AND release:[5.2.0.0 TO 5.6.0.3]')
    releases += client.packages.search.advanced(key, 'name:redhat-release-server AND version:6Server AND release:6.0.0.37.el6')
    releases += client.packages.search.advanced(key, 'name:redhat-release-workstation AND version:6Workstation AND release:6.0.0.37.el6')

    print "systemid, Profile name, version-release"
    systems = []
    for p in releases:
        for s in client.system.listSystemsWithPackage(key, p['id']):
            print str(s['id']) + ", " + s['name'] + ", " + p['version'] + "-" + p['release']

    client.auth.logout(key)

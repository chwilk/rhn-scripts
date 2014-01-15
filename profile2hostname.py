#!/usr/bin/python
# Renames machines' profiles by their hostnames (searches for hostnames)
import xmlrpclib
import getpass
import datetime

SATELLITE_URL = "http://YOUR.SATELLITE.SERVER/rpc/api"
SATELLITE_LOGIN = "username"
SATELLITE_PASSWORD = "password"


if __name__ == "__main__":
    client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
    SATELLITE_LOGIN = str(raw_input("RHN Userid: ")).rstrip()
    SATELLITE_PASSWORD = getpass.getpass() 

    print "Type q or EOF to exit\n"
    hostname = str(raw_input("FQDN to search > ")).rstrip()
    while(hostname not in ['q', 'quit', 'exit', 'Q', '']):
        key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
        result_array = client.system.search.hostname(key, hostname)
        i = 0
	for i in xrange(0,len(result_array)):
	    if (result_array[i]['hostname'] == hostname):
		print "Found FQDN hostname with profile name " + str(result_array[i]['name'])
		print "systemID ",
		print result_array[i]['id']
		print "last check in: ",
		print result_array[i]['last_checkin']
		choice =  str(raw_input("Rename? [Y/n/delete]: ")).rstrip()
		if choice == 'delete':
		    print "Deleting system with id: ",
		    print result_array[i]['id']
		    client.system.deleteSystem(key, result_array[i]['id'])
		elif choice in ['y', 'Y', '']:
		    print "Renaming system with id: ",
		    print result_array[i]['id']
		    client.system.setProfileName(key, result_array[i]['id'], result_array[i]['hostname'])
		else:
		    print "Skipping ",
		    print result_array[i]['id']
		i += 1
	    else:
		if i == 0:
		    print "Could not find that hostname. Did you run rhn-profile-sync after updating the hostname?"
	hostname = str(raw_input("FQDN to search > ")).rstrip()

    client.auth.logout(key)

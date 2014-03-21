#!/usr/bin/env python
# Generates a kickstartable list of yum package groups and ungrouped RPMs
# from current system
#
# Author: Chandler Wilkerson <chwilk@rice.edu>
#
import yum

yb = yum.YumBase()
yb.doConfigSetup()
yb.doTsSetup()
yb.doRpmDBSetup()
    
# Grab Installed Package List (ipl)
ipl=set([pkg[0] for pkg in yb.rpmdb.pkglist])
grppkgs = set([])
# Grab Group List (gl)
gl=yb.doGroupLists()
# First index of gl is Installed Group List (igl)
igl=gl[0]

# Make sure we still are accounting for Core (sometimes packages get removed)
gotcore = False
for grp in igl:
    if grp.groupid == 'core': gotcore = True

if not gotcore:
    for grp in gl[1]:
        if grp.groupid == 'core':
           igl.append(grp)

# Find leaves of dependency tree (by pruning any package whose dependencies are in the list)
loners = ipl.copy()
for pkg in list(loners):
    deps= yb.findDeps(yb.returnInstalledPackagesByDep(pkg)).values()[0].keys()
    for dep in [d[0] for d in deps] :
        if dep in loners:
            loners.remove(pkg)
            break

# Prune from installed package list any packages installed by a group in our list
for grp in igl:
    for pkg in grp.mandatory_packages:
        if pkg in loners:
            loners.remove(pkg)
    for pkg in grp.default_packages:
        if pkg in loners:
            loners.remove(pkg)
# Print a kickstartable group list first
    print '@'+grp.groupid
 
# Print remainder of packages not covered by above groups or upstream dependents of such packages.
for pkg in loners:
   print pkg

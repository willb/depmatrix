#!/usr/bin/env python

import re
import sys
from collections import defaultdict

start_project_pattern = re.compile(".INFO. --- [^@]+@ ([^ ]+) ---")
dependency_pattern = re.compile(".INFO.    ([a-z].*)")
current_project = "project"

results = defaultdict(lambda: set())
projects = set()

if __name__ == "__main__":
    for line in sys.stdin:
        match = start_project_pattern.match(line)
        if match is not None:
            current_project, = match.groups(1)
            current_project = current_project.replace("_2.10","")
            projects.add(current_project)
        else:
            match = dependency_pattern.match(line)
            if match is not None:
                configuration = ""
                library, = match.groups(1)
                library = library.split(":")
                if len(library) == 6:
                    configuration = library[3]
                    del library[3]
                key = ",".join(library + [configuration])
                results[key].add(current_project)

    allprojects = list(projects)
    allprojects.sort()

    print "Group ID, Artifact ID, Artifact Kind, Version, Configuration, Profile,", ",".join(allprojects)
    
    for (k, pjs) in results.items():
        reqs = [(prj in pjs and "Yes") or "No" for prj in allprojects]
        print(k + "," + ",".join(reqs))
        

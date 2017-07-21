#!/usr/bin/env python3.6

import sys

from jira import JIRA
jira = JIRA('http://localhost/jira', basic_auth=('admin', 'adm8nf52!'))

def getIssueKeys():
    return [i.key for i in jira.search_issues('')]

def checkBranchName(branchName):
    branchParts = branchName.strip().split('-', 2)
    if len(branchParts) < 3:
        return False
    if len(branchParts[2]) == 0:
        return False
    issueKey = branchParts[0] + "-" + branchParts[1]
    if issueKey not in getIssueKeys():
        return False
    return True

if __name__ == '__main__':
    for line in sys.stdin:
        (old, new, branch) = line.strip().split(" ", 2)
        if int(old, 16) == 0:
            # New branch, check name
            (refs, heads, branchName) = branch.split("/", 2)
            if not checkBranchName(branchName):
                print("Error: invalid branch name '" + branchName + "'")
                sys.exit(1)

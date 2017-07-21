#!/usr/bin/env python3.6

import subprocess
import sys

from jira import JIRA
jira = JIRA('http://localhost/jira', basic_auth=('admin', 'adm8nf52!'))


def get_issue_keys():
    return [i.key for i in jira.search_issues('')]


def check_commit_msg(commit_msg):
    cm_parts = commit_msg.strip().split(': ', 1)
    if len(cm_parts) < 2:
        return False
    if len(cm_parts[1]) == 0:
        return False
    if cm_parts[0] not in get_issue_keys():
        return False
    return True


if __name__ == '__main__':
    for line in sys.stdin:
        (old, new, ref) = line.strip().split(' ', 2)
        if int(old, 16) == 0 or int(new, 16) == 0:
            # New branch/branch deleted
            sys.exit(0)
        else:
            revs = old + "..." + new
            proc = subprocess.run(['git', 'rev-list', '--oneline',
                                   '--first-parent', revs],
                                  stdout=subprocess.PIPE)
            for line in proc.stdout.decode("utf-8").splitlines():
                line_parts = line.strip().split(' ', 1)
                if not check_commit_msg(line_parts[1]):
                    print("Invalid commit message format for commit %s"
                          % line_parts[0])
                    sys.exit(1)

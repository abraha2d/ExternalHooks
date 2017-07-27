# ExternalHooks

```
System Requirements:
RAM: 10GB
Storage: 12GB

RHEL 7.3 on VirtualBox

Follow RHEL on VBox install guide:
- Server with GUI + Java, PostgreSQL, Development Tools, Security Tools
- Security Policy: Common Profile for General-Purpose Systems

Do PostgreSQL initdb

Enable rhel-7-server-extras-rpms
Install EPEL repository
Install IUS repository
Swap git with git2u (v2.10.2 from ius-archive, v2.11+ causes issues with the 02-check-commit-message hook)
Install python36u and python36u-pip

Follow Atlassian installation guides

Install "External Hooks" Bitbucket plugin
Clone external hooks to $STASH_HOME/external-hooks/
Configure external hooks to point to external-hook.py (safe mode on), params = one of merge-check.d/pre-receive.d/post-receive.d
```

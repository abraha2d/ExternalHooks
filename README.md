# External Hooks

```
VirtualBox VM:
4 processors, 12GB RAM, 20GB HDD

Install RHEL:

    Connect to network

    Software Selection: Server with GUI
        E-mail Server
        Java Platform
        PostgreSQL Database Server
        Development Tools
        Security Tools

    Kdump: disabled

    Security Policy: Common Profile for General-Purpose Systems
    
    No root password

    Full name: User
    Username: user
    Make this user administrator
    Password: RHELatl17!

Reboot

--------------------------------------------------------------------------------

Disable lock screen and screen power saving:
    Settings > Privacy > Screen Lock > Automatic Screen Lock: Off
    Settings > Power > Blank: Never


Enable additional software repositories:
sudo subscription-manager repos --enable rhel-server-rhscl-7-rpms
sudo subscription-manager repos --enable rhel-7-server-optional-rpms
sudo subscription-manager repos --enable rhel-7-server-extras-rpms

Install the latest updates:
sudo yum -y update

Reboot

--------------------------------------------------------------------------------

Install VirtualBox Guest Additions:
    Select Insert Guest Additions CD image from the Devices menu of the VM window.
    A dialog box will pop up asking you if you want to run the software on the virtual CD. Click Run.
    Enter the password for the root user when prompted. Then click Authenticate.
    A Terminal window will appear with the install process running inside of it. When the process it complete you will be prompted to hit Return to close the window.
    Eject the virtual CD by right clicking on its icon on the desktop and selecting Eject.

Initialize PostgreSQL database:
sudo postgresql-setup initdb
sudo nano /var/lib/pgsql/data/pg_hba.conf
# Modify this line:
#host    all             all      	127.0.0.1/32            ident
# to look like this line:
#host    all             all      	127.0.0.1/32            md5
sudo systemctl enable postgresql.service

Install EPEL and IUS repositories:
cd Downloads
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
wget https://rhel7.iuscommunity.org/ius-release.rpm
sudo yum -y install epel-release-latest-7.noarch.rpm ius-release.rpm
sudo yum -y update

Reboot

--------------------------------------------------------------------------------

Set up PostgreSQL databases for Atlassian apps:

sudo su - postgres
psql
CREATE ROLE jiradbuser WITH LOGIN PASSWORD 'jellyfish' VALID UNTIL 'infinity';
CREATE DATABASE jiradb WITH ENCODING 'UNICODE' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;
GRANT ALL PRIVILEGES ON DATABASE jiradb to jiradbuser;
CREATE ROLE bitbucketuser WITH LOGIN PASSWORD 'jellyfish' VALID UNTIL 'infinity';
CREATE DATABASE bitbucket WITH ENCODING='UTF8' OWNER=bitbucketuser CONNECTION LIMIT=-1;
GRANT ALL PRIVILEGES ON DATABASE bitbucket to bitbucketuser;
CREATE ROLE confluenceuser WITH LOGIN PASSWORD 'jellyfish' VALID UNTIL 'infinity';
CREATE DATABASE confluence WITH ENCODING='UTF8' OWNER=confluenceuser CONNECTION LIMIT=-1;
GRANT ALL PRIVILEGES ON DATABASE confluence to confluenceuser;
\q
createuser -S -d -r -P -E bamboouser
# Enter password: jellyfish
createdb -O bamboouser bamboo
exit

Install supported version of Git (v2.10.2):

sudo yum -y --enablerepo=ius-archive swap git git2u-2.10.2

--------------------------------------------------------------------------------

Prepare Atlassian apps for installation:
cd Downloads
chmod +x atlassian-*.bin

Install Atlassian apps:

# Pick all the default options for the following 3
sudo ./atlassian-jira-software-*.bin
sudo ./atlassian-bitbucket-*.bin

sudo useradd --create-home -c "Bamboo role account" bamboo
sudo mkdir -p /opt/atlassian/bamboo
sudo chown bamboo: /opt/atlassian/bamboo
cp atlassian-bamboo-*.tar.gz /tmp

sudo su - bamboo
cd /opt/atlassian/bamboo
tar zxvf /tmp/atlassian-bamboo-*.tar.gz
ln -s atlassian-bamboo-*/ current
nano current/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties
# uncomment and set bamboo.home=/var/atlassian/application-data/bamboo
exit

sudo mkdir /var/atlassian/application-data/bamboo
sudo chown bamboo: /var/atlassian/application-data/bamboo

sudo nano /etc/init.d/bamboo

# Paste the following FROM HERE
#!/bin/sh
set -e
### BEGIN INIT INFO
# Provides: bamboo
# Required-Start: $local_fs $remote_fs $network $time
# Required-Stop: $local_fs $remote_fs $network $time
# Should-Start: $syslog
# Should-Stop: $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Atlassian Bamboo Server
### END INIT INFO
# INIT Script
######################################

# Define some variables
# Name of app ( bamboo, Confluence, etc )
APP=bamboo
# Name of the user to run as
USER=bamboo
# Location of application's bin directory
BASE=/opt/atlassian/bamboo/current

case "$1" in
  # Start command
  start)
    echo "Starting $APP"
    /bin/su - $USER -c "export BAMBOO_HOME=${BAMBOO_HOME}; $BASE/bin/startup.sh &> /dev/null"
    ;;
  # Stop command
  stop)
    echo "Stopping $APP"
    /bin/su - $USER -c "$BASE/bin/shutdown.sh &> /dev/null"
    echo "$APP stopped successfully"
    ;;
   # Restart command
   restart)
        $0 stop
        sleep 5
        $0 start
        ;;
  *)
    echo "Usage: /etc/init.d/$APP {start|restart|stop}"
    exit 1
    ;;
esac

exit 0
# TO HERE

sudo chmod a+x /etc/init.d/bamboo
sudo /sbin/chkconfig --add bamboo
sudo service bamboo start

--------------------------------------------------------------------------------

JIRA setup: localhost:8080/

Pick "I'll set it up myself"

Database Connection: My Own Database
Database Type: PostgreSQL
Hostname: 127.0.0.1
Database: jiradb
Username: jiradbuser
Password: jellyfish

Application Title: JIRA

Your License Key:
AAABbg0ODAoPeNp9UUtPwkAQvu+vaOJFD9v0gfJINhHbjSkphVA0mnhZywCrpW1mtyj/3kJrBHkcv
92Z7zVXsdDGoEwNp2vYtz33rme5hudPDcey22SBANkyLwpAM5QJZAr4TGqZZ4xHUz4ZT4KYk6hcv
QOO5k8KUDFqkw+Jwjx6HZeYLIUCX2hgW3pqtalrkYZ4uikgEitg3mg45BMv6Ie/X/y7kLjZ2+tQp
0O8PNMi0XwoZMo+YX2/qAaSpQmzksSAa8DAZw/hY0RbltuiYfvllcZuq1/bKzCflYk2t4CqfK6/B
IJZ8ck1MI0l1GPnU5/o5lSEyl2mIRNZcibGBTdHFTY6Va4w8GMe0dC2rE7XtWxSIXb4coE41gI1I
JuLVAEZ4UJkUoldQh9WOfEQduj/qdJa/7mys511DkqAKicWKFXTnw8qQVnsWAfBpG/EjbxxXZ/n5
q1n8LVIy51W7ffcAU5Vuy++v/fHWeMfv/r7SDAsAhRd37rtSDXdN55swVq62Sghxofn/gIUTqBei
PPXAOdldXh3GXSuZEYK2PI=X02ht

Full name: Administrator
Email Address: <redacted>
Username: admin
Password: adm8nf52!

Select "Create sample project"
Select "Project management"
Name: Sample

--------------------------------------------------------------------------------

Bitbucket setup: localhost:7990/

Database: External
Hostname: 127.0.0.1
Database name: bitbucket
Database username: bitbucketuser
Database password: jellyfish

License key: I have a Bitbucket license key
AAABKA0ODAoPeNptkE1rwkAQhu/7KxZ6aQ8rSdQahYXGbA4p0dSmH1B6GbejLsZV9iPUf9/YWFqKh
4Fh5p1n5p2rChy99zWNxjQcTgaDyXBIU/FEoyAcEYFWGnVwaq/5VLmll1t09LpC06C5eZ/QrIHaw
6lPUoPfiQCH/DTNghHrByTdawfSZTNQNd9ic7duBXLTww9Pfse5Mx6JdWA3vVatGuwqtZKoLb6gs
SdVRFqMdqhBS8w+D8oc/+yLWRST0qxBK9tRBe72Z2rRkZ6OB5zDDnlazmbZY5onBen85IJPx0nJk
sX0lUXF7Rtb5CIhVTbnbbAiDIJ43A9jcia1+iIXF1uXL+vuqBwYh4avoLY/jud+t0RTrp5t65Ozk
Dx4Izdg8f8zvwAO/otrMC0CFFHX9W6HGESvWSbSfqXHoFRTisVAAhUAjI/OxEk8GT9vMvK2n4tP/
N6cWc8=X02eu

Username: admin
Full name: Administrator
Email address: <redacted>
Password: adm8nf52!

JIRA base URL: http://localhost:8080
JIRA administrator username: admin
JIRA password: adm8nf52!
Select "Use JIRA as my user database"

Select "Create project"
Project name: Sample

Select "Create repository"
Name: Sample

--------------------------------------------------------------------------------

External Hooks setup:

Bitbucket > Settings > Find new add-ons > Search for "External Hooks" by Stanislav Seletskiy > Install

sudo yum -y install python36u-pip
sudo pip3.6 install jira

sudo su - atlbitbucket
git clone https://github.com/abraha2d/external-hooks.git

Bitbucket > Repositories > Sample/Sample > Settings > Hooks >

External Pre Receive Hook > Enabled
Executable: external-hook.py
Select "Safe mode"
Positional parameters: /var/atlassian/application-data/bitbucket/external-hooks/pre-receive.d/

--------------------------------------------------------------------------------

Have fun!
```

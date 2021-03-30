import logging

from lib.filters import TagFilter
from lib.models import Password, Login, Scope, Credential
from lib.context import Context
import lib.pipelines
from lib.outputs import ListOutput

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    scope = Scope(company='Paniccrew', keywords=['hacking', 'bumm', 'karlsruhe'])

    with open('data/default_admin_users.txt') as a_file:
        admin_names = a_file.read().strip().split("\n")

    with open('data/default_admin_passwords.txt') as p_file:
        admin_passwords = p_file.read().strip().split("\n")

    with open('data/default_admin_credentials.txt') as p_file:
        admin_credentials = p_file.read().strip().split("\n")

    logins = []
    passwords = []
    credentials = []

    for admin in admin_names:
        logins.append(Login(value=admin, tags=('default', 'admin'), reliability=0.75))

    for pw in admin_passwords:
        passwords.append(Password(value=pw, tags=('default', 'admin'), reliability=0.75))

    for row in admin_credentials:
        username, password = row.split(":", 1)
        l = Login(value=username, tags=('default', 'admin'), reliability=1.0)
        p = Password(value=username, tags=('default', 'admin'), reliability=1.0)
        credentials.append(Credential(login=l, password=p))

    c1 = Context(scope=scope, logins=logins, passwords=passwords, credentials=credentials,
                 pipelines=(lib.pipelines.admin_default, lib.pipelines.admin_company),
                 outputs=(ListOutput(destination=open('output/admin_userpass.txt', "w")),))
    c1.build()

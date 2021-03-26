from dataclasses import dataclass

@dataclass
class Password(object):
    reliability: float#: float = 1.0
    value: str
    tags: list

@dataclass
class Login(object):
    reliability: float  #: float = 1.0
    value: str
    tags: list

@dataclass
class Credential(object):
    login: Login
    password: Password


@dataclass
class Scope(object):
    company: str
    keywords: list

@dataclass
class Context(object):
    scope: Scope
    logins: list
    passwords: list
    mergers: list

    @property
    def credentials(self):
        creds = []
        for merger in self.mergers:
            creds += merger.combinations(self.logins, self.passwords)
        return creds


class CredentialMerger(object):
    def combinations(self):
        pass

class CrossCredentialMerger(CredentialMerger):

    def combinations(self, logins, passwords):
        for login in logins:
            for password in passwords:
                yield Credential(login=login, password=password)


if __name__ == '__main__':
    scope = Scope(company='Paniccrew', keywords=['hacking', 'salatschleuder', 'karlsruhe'])


    with open('data/default_admins.txt') as a_file:
        admin_names = a_file.read().strip().split("\n")

    with open('data/default_passwords.txt') as p_file:
        default_passwords = p_file.read().strip().split("\n")

    logins = []
    passwords = []

    for admin in admin_names:
        logins.append(Login(value=admin, tags=('default', 'admin'), reliability=1.0))

    for pw in default_passwords:
        passwords.append(Password(value=pw, tags=('default', 'admin'), reliability=1.0))

    c1 = Context(scope=scope, logins=logins, passwords=passwords, mergers=[CrossCredentialMerger()])
    print(c1.credentials)
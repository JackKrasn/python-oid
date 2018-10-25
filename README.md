# py-oid

Питоновский пакет для работы с  ldap Oracle Internet Directory. 

## Getting Started
Пакет размещен в менеджере репозиториев [Nexus](https://bs-nexus.ftc.ru/)  

### Prerequisites

Должны быть установлены модули ldap, python-ldap.

> How to install module ldif https://stackoverflow.com/questions/4768446/i-cant-install-python-ldap

Установка на Fedora.

До установки модуля ldif необходимо установить пакет **openldap-devel** 
~~~
sudo -E  dnf install openldap-devel
~~~

Установить пакет python-ldap

~~~
pip install python-ldap
~~~

Установить пакет ldap

~~~
pip install ldap
~~~

### Installing
Установить пакет
~~~
pip install oracledb
~~~

## Deployment
Импортировать пакет
~~~
import ldapoid
~~~
Пример создания tns алиаса
```python
from ldapoid import ld
import logging

server='ldap_seerver'
dn='cn=orcladmin, cn=Users, dc=ftc, dc=ru'
passw='password'

dn_domain='dc=ftc, dc=ru'
conn = ld.connection(server, dn, passw)
ld.create_dbalias(conn, 
                 dn_domain=dn_domain, 
                 dbalias='182_PY_TEST2',
                 host='hostname', 
                 lisport='port_number', 
                 sn='service_name'.lower())
```

## Versioning

Я использую [Семантическое Версионирование 2.0.0](https://semver.org/lang/ru/)

Достпуные релизы tags on this repository

## Authors

Evgeniy Krasnukhin (e.krasnukhin@cft.ru)
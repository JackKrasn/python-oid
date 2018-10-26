# -*- coding: utf-8 -*-
import ldap  # pip install ldap
import ldif  # pip install python-ldap
import ldap.modlist
import logging
import utils
import config

# How to install module ldif https://stackoverflow.com/questions/4768446/i-cant-install-python-ldap
# Fedora:  sudo -E  dnf install openldap-devel
# after install openldap-devel install module python-ldap
# pip install python-ldap


class MyLDIF(ldif.LDIFParser, object):
    """
    Класс перегружен для возможности импорта ldif файла в ldap.
    Из шаблона формируется файл ldif и импортируется в ldap.
    """
    def __init__(self, in_file, conn):
        """
        Конструктор класса
        :param in_file: файл в формате ldif, который необходимо импортировать
        :param conn: объект коннект к ldap
        """
        super(MyLDIF, self).__init__(in_file)
        # self.conn = ldap.initialize('ldap://' + ldap_server)
        # self.conn.simple_bind_s(dn, pw)
        self.conn = conn

    def handle(self, dn, entry):
        # необходимо преобразовывать unicode в byte string utf8 в противном случае возникает ошибка
        # Поскольку entry - это словарь списков, то для декодирования словаря
        # {k: [s.encode('utf-8') for s in v] for k,v in entry.iteritems()}
        #
        modlist = ldap.modlist.addModlist({k: [s.encode('utf-8') for s in v] for k, v in entry.iteritems()})
        self.conn.add_s(dn, modlist)


def create_dbalias(ldap_conn, dn_domain=None, dbalias=None, host=None, lisport=None, sn=None):
    """
    Создание алиса базы данных в oracle ldap
    :param ldap_conn: объект коннект к ldap серверу
    :param dn_domain: dn в формате 'cn=OracleContext, dc=ftc, dc=ru'
    :param dbalias: алиас базы данных
    :param host: имя хоста, где расположена БД
    :param lisport: номер порта листенера
    :param sn: service name для подключения
    """
    dn = 'cn=' + dbalias + ', cn=OracleContext, ' + dn_domain
    # словарь для формирования ldif файла из шаблона
    tpl_context = {'DN': dn,
                   'DBALIAS': dbalias,
                   'HOST': host,  #.split('.')[0],  # + '.ftc.ru',  # для гарантированного добавления ftc.ru к имени сервера
                   'LISPORT': lisport,
                   'SERVICE_NAME': sn}
    try:
        # Если алиас уже существует, то ничего не делать, в противном случае импортировать ldif файл
        ldap_conn.search_s(dn, ldap.SCOPE_SUBTREE)
        logging.warning('%s already exists', dbalias)
    except ldap.NO_SUCH_OBJECT:
        ldif_file = utils.gen_from_tpl(config.TPL_DIR, config.TPL_DN, **tpl_context)
        parser = MyLDIF(ldif_file, ldap_conn)
        parser.parse()
        logging.info('tns %s successfully added', dbalias)


def delete_dbalias(ldap_conn, dn_domain=None, dbalias=None):
    # dn = 'cn=' + dbalias + ',cn=Oraclecontext, dc=ftc,dc=ru'
    dn = 'cn=' + dbalias + ', cn=OracleContext, ' + dn_domain
    try:
        search = ldap_conn.search_s(dn, ldap.SCOPE_SUBTREE )
        for dn_d, _ in search:
            try:
                ldap_conn.delete_s(dn_d)
            except ldap.LDAPError, e:
                logging.error('%s', e.message['desc'])
    except ldap.NO_SUCH_OBJECT:
        logging.warning('no such dbalias %s in ldap', dbalias)


def connection(ldap_server, dn, passw):
    conn = ldap.initialize('ldap://' + ldap_server)
    conn.simple_bind_s(dn, passw)
    return conn

# if __name__ == '__main__':
#     # Подключение  к ldap серверу
#     conn = ldap.initialize('ldap://' + ldap_server)
#     conn.simple_bind_s(dn, pw)
#     conn.search_s('cn=KEA_TST_122, cn=OracleContext, dc=ftc, dc=ru', ldap.SCOPE_SUBTREE )
    #delete_dbalias(conn, dbalias='KEA12C')
    #create_dbalias(conn, dbalias='KEA_122_CDB', host='kealnx.ftc.ru', lisport='1522', sn='kea122c')
import os
from nose.tools import eq_
from sqlautocode.declarative import ModelFactory
from sqlalchemy.orm import class_mapper
testdb = 'sqlite:///'+os.path.abspath(os.path.dirname(__file__))+'/data/devdata.db'
#testdb = 'postgres://postgres@localhost/TestSamples'

from base import make_test_db

class DummyConfig:


    def __init__(self, engine=testdb):
        self.engine  = engine

    example = True
    schema = None
    interactive = None
#    schema = ['pdil_samples', 'pdil_tools']


class TestModelFactory:

    def setup(self):
        self.config = DummyConfig()
        self.factory = ModelFactory(self.config)

    def test_tables(self):
        tables = sorted(self.factory.tables)
        eq_(tables,  [u'tg_group', u'tg_group_permission', u'tg_permission', u'tg_town', u'tg_user', u'tg_user_group'])

    def _setup_all_models(self):
        return self.factory.models

    def test_create_model(self):
        self.factory.used_model_names = []
        self.factory.used_table_names = []

        Group      = self.factory.create_model(self.factory._metadata.tables['tg_group'])
        Permission = self.factory.create_model(self.factory._metadata.tables['tg_permission'])
        Town       = self.factory.create_model(self.factory._metadata.tables['tg_town'])
        User       = self.factory.create_model(self.factory._metadata.tables['tg_user'])

        class_mapper(Town)
        class_mapper(User)

        t = Town(town_name="Arvada")
        u = User(tg_town=t)
        assert u.tg_town.town_name == 'Arvada'

    def test_get_many_to_many_tables(self):
        tables = sorted([table.name for table in self.factory.get_many_to_many_tables()])
        eq_(tables, [u'tg_group_permission', u'tg_user_group'])

    def test_get_related_many_to_many_tables(self):
        tables = [table.name for table in self.factory.get_related_many_to_many_tables('tg_user')]
        eq_(tables, [u'tg_user_group'])

    def test_get_foreign_keys(self):
        columns = [column[0].name for column in self.factory.get_foreign_keys(self.factory._metadata.tables['tg_user']).values()]
        eq_(columns, ['town_id'])


    def test_model___repr__(self):
        models = sorted(self._setup_all_models())
        for model in models:
            if model.__name__=='TgUser':
                User = model
        r = User.__repr__()
        print r
        expected = """\
class TgUser(DeclarativeBase):
    __tablename__ = 'tg_user'

    #column definitions
    created = Column(u'created', TIMESTAMP(timezone=False))
    display_name = Column(u'display_name', VARCHAR(length=255, convert_unicode=False, assert_unicode=None))
    email_address = Column(u'email_address', VARCHAR(length=255, convert_unicode=False, assert_unicode=None), nullable=False)
    password = Column(u'password', VARCHAR(length=80, convert_unicode=False, assert_unicode=None))
    town_id = Column(u'town_id', INTEGER(), ForeignKey('tg_town.town_id'))
    user_id = Column(u'user_id', INTEGER(), primary_key=True, nullable=False)
    user_name = Column(u'user_name', VARCHAR(length=16, convert_unicode=False, assert_unicode=None), nullable=False)

    #relation definitions
    tg_town = relation('TgTown')
    tg_groups = relation('TgGroup', secondary=tg_user_group)
"""
        eq_(r.strip(), expected.strip())

    def test__repr__(self):

        r = repr(self.factory)
        print r
        expected = """\
#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine('sqlite:////Users/percious/oss/tgtut/src/sqlautocode/sqlautocode/tests/data/devdata.db')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

tg_group_permission = Table(u'tg_group_permission', metadata,
    Column(u'group_id', INTEGER(), ForeignKey('tg_group.group_id'), primary_key=True, nullable=False),
    Column(u'permission_id', INTEGER(), ForeignKey('tg_permission.permission_id'), primary_key=True, nullable=False),
)

tg_user_group = Table(u'tg_user_group', metadata,
    Column(u'user_id', INTEGER(), ForeignKey('tg_user.user_id'), primary_key=True, nullable=False),
    Column(u'group_id', INTEGER(), ForeignKey('tg_group.group_id'), primary_key=True, nullable=False),
)

class TgGroup(DeclarativeBase):
    __tablename__ = 'tg_group'

    #column definitions
    created = Column(u'created', TIMESTAMP(timezone=False))
    display_name = Column(u'display_name', VARCHAR(length=255, convert_unicode=False, assert_unicode=None))
    group_id = Column(u'group_id', INTEGER(), primary_key=True, nullable=False)
    group_name = Column(u'group_name', VARCHAR(length=16, convert_unicode=False, assert_unicode=None), nullable=False)

    #relation definitions
    tg_permissions = relation('TgPermission', secondary=tg_group_permission)
    tg_users = relation('TgUser', secondary=tg_user_group)


class TgPermission(DeclarativeBase):
    __tablename__ = 'tg_permission'

    #column definitions
    description = Column(u'description', VARCHAR(length=255, convert_unicode=False, assert_unicode=None))
    permission_id = Column(u'permission_id', INTEGER(), primary_key=True, nullable=False)
    permission_name = Column(u'permission_name', VARCHAR(length=16, convert_unicode=False, assert_unicode=None), nullable=False)

    #relation definitions
    tg_groups = relation('TgGroup', secondary=tg_group_permission)


class TgTown(DeclarativeBase):
    __tablename__ = 'tg_town'

    #column definitions
    town_id = Column(u'town_id', INTEGER(), primary_key=True, nullable=False)
    town_name = Column(u'town_name', VARCHAR(length=255, convert_unicode=False, assert_unicode=None))

    #relation definitions


class TgUser(DeclarativeBase):
    __tablename__ = 'tg_user'

    #column definitions
    created = Column(u'created', TIMESTAMP(timezone=False))
    display_name = Column(u'display_name', VARCHAR(length=255, convert_unicode=False, assert_unicode=None))
    email_address = Column(u'email_address', VARCHAR(length=255, convert_unicode=False, assert_unicode=None), nullable=False)
    password = Column(u'password', VARCHAR(length=80, convert_unicode=False, assert_unicode=None))
    town_id = Column(u'town_id', INTEGER(), ForeignKey('tg_town.town_id'))
    user_id = Column(u'user_id', INTEGER(), primary_key=True, nullable=False)
    user_name = Column(u'user_name', VARCHAR(length=16, convert_unicode=False, assert_unicode=None), nullable=False)

    #relation definitions
    tg_town = relation('TgTown')
    tg_groups = relation('TgGroup', secondary=tg_user_group)


#example on how to query your Schema
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)()
objs = session.query(TgGroup).all()
print 'All TgGroup objects: %s'%objs
"""
        assert expected in r, r


class TestModelFactoryNew:

    def setup(self):
        self.metadata = make_test_db()
        engine = self.metadata.bind
        self.config = DummyConfig(engine)
        self.factory = ModelFactory(self.config)
        self.factory.models

    def test_tables(self):
        tables = sorted(self.factory.tables)
        eq_(tables,  [u'environment', u'report', u'ui_report'])

    def test_setup_all_models(self):
        assert len(self.factory.models) == 3

    def test_repr_environ_model(self):
        print self.factory.models
        s = self.factory.models[0].__repr__()
        assert s == """\
class Environment(DeclarativeBase):
    __tablename__ = 'environment'

    #column definitions
    database_host = Column(u'database_host', VARCHAR(length=100, convert_unicode=False, assert_unicode=None), nullable=False)
    database_pass = Column(u'database_pass', VARCHAR(length=100, convert_unicode=False, assert_unicode=None), nullable=False)
    database_port = Column(u'database_port', VARCHAR(length=5, convert_unicode=False, assert_unicode=None), nullable=False)
    database_sid = Column(u'database_sid', VARCHAR(length=32, convert_unicode=False, assert_unicode=None), nullable=False)
    database_user = Column(u'database_user', VARCHAR(length=100, convert_unicode=False, assert_unicode=None), nullable=False)
    environment_id = Column(u'environment_id', NUMERIC(precision=10, scale=0, asdecimal=True), primary_key=True, nullable=False)
    environment_name = Column(u'environment_name', VARCHAR(length=100, convert_unicode=False, assert_unicode=None), nullable=False)

    #relation definitions
    reports = relation('Report', secondary=ui_report)
""", s

    def test_repr_report(self):
        s = self.factory.models[1].__repr__()
        assert s == """class Report(DeclarativeBase):
    __tablename__ = 'report'

    #column definitions
    created_by = Column(u'created_by', NUMERIC(precision=10, scale=0, asdecimal=True), nullable=False)
    created_date = Column(u'created_date', DATETIME(timezone=False), nullable=False)
    deleted = Column(u'deleted', NUMERIC(precision=1, scale=0, asdecimal=True), nullable=False)
    deleted_by = Column(u'deleted_by', NUMERIC(precision=10, scale=0, asdecimal=True))
    deleted_date = Column(u'deleted_date', DATETIME(timezone=False))
    environment_id = Column(u'environment_id', NUMERIC(precision=10, scale=0, asdecimal=True), ForeignKey('environment.environment_id'), nullable=False)
    report_description = Column(u'report_description', VARCHAR(length=4000, convert_unicode=False, assert_unicode=None))
    report_id = Column(u'report_id', NUMERIC(precision=10, scale=0, asdecimal=True), primary_key=True, nullable=False)
    report_name = Column(u'report_name', VARCHAR(length=50, convert_unicode=False, assert_unicode=None), nullable=False)
    updated_by = Column(u'updated_by', NUMERIC(precision=10, scale=0, asdecimal=True), nullable=False)
    updated_date = Column(u'updated_date', DATETIME(timezone=False), nullable=False)

    #relation definitions
    environment = relation('Environment')
    environments = relation('Environment', secondary=ui_report)
""", s

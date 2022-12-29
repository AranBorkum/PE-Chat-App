import os
from typing import MutableMapping, Union, Type
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session

import config
from db.base import Base
from db import user, messages

ALL_MODULES_WITH_MODELS = [
    user,
    messages,
]


class EngineFactory:
    def __init__(self, **kwargs):
        self._kwargs = dict(echo=True, future=True)
        self._kwargs.update(kwargs)

    def create_from_envvars(self, **kwargs) -> Engine:
        # construct PostgreSQL from envvars
        return self.create_engine(self.uri_from_envvars(), **kwargs)

    def create_from_config(self, env_filename, **kwargs) -> Engine:
        # construct from config (.env reading)
        return self.create_engine(
            self.uri_from_config(env_filename),
            **kwargs,
        )

    def uri_from_config(self, env_filename) -> str:
        return self.uri_from_dict(config.get_values(env_filename))

    def create_engine(self, uri: str, **kwargs) -> Engine:
        kw = dict(self._kwargs)
        kw.update(kwargs)
        return create_engine(uri, **kw)

    @staticmethod
    def construct_uri(
        *,
        driver: str,
        username: str,
        password: str,
        host: str,
        port: Union[int, str],
        dbname: str
    ) -> str:
        db_uri = "{driver}://{username}:{password}@{host}:{port}/{dbname}".format(
            driver=driver,
            username=username,
            password=quote_plus(password),
            host=host,
            port=port,
            dbname=dbname,
        )

        return db_uri

    def uri_from_envvars(self) -> str:
        return self.uri_from_dict(os.environ)

    def uri_from_dict(self, container: MutableMapping) -> str:
        # works with any container that has a .get method, including os.environ
        return self.construct_uri(
            driver=container.get("DB_DRIVER", "postgresql"),
            username=container.get("DB_USER"),
            password=container.get("DB_PASS"),
            host=container.get("DB_HOST"),
            port=container.get("DB_PORT"),
            dbname=container.get("DB_NAME"),
        )


def get_or_create(session: Session, model: Type[Base], **kwargs) -> Base:
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    return instance

#!/usr/bin python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categorie(Base):
    __tablename__ = 'categorie'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    slug = Column(String(80), nullable=False)
    categorie_id = Column(Integer, ForeignKey('categorie.id'))
    categorie = relationship(Categorie)
    description = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'categorie': self.categorie.name,
            'description': self.description
        }


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(160))


engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.create_all(engine)

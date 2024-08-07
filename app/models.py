from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String, index=True)
    revenue = Column(Integer)
    employees = Column(Integer)
    homepage_base_url = Column(String, unique=True)

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String, index=True)
    date = Column(String)
    location = Column(String)
    event_url = Column(String, unique=True)

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    job_title = Column(String)
    email = Column(String, unique=True)
    homepage_base_url = Column(String, ForeignKey('companies.homepage_base_url'))

    company = relationship("Company", back_populates="employees")

Company.employees = relationship("Person", order_by=Person.id, back_populates="company")

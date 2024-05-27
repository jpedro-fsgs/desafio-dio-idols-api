from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, relationship

def get_session():
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()

engine = create_engine('sqlite:///./idols.db')

Base = declarative_base()

class Idol(Base):
    __tablename__ = 'idol'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stage_name = Column(String)
    real_name = Column(String)
    group_id = Column(Integer, ForeignKey('group.id'))
    
    group = relationship("Group", back_populates="idols")

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    company = Column(String, index=True)
    
    idols = relationship("Idol", back_populates="group")

Base.metadata.create_all(engine)
from fastapi import Depends
from sqlalchemy import create_engine
from api.schema import Group, Idol, get_session
from sqlalchemy.orm import joinedload, Session


def test_schemas_validatet():
    grupo = Group(name="MIX6", company="JYP", id=150)
    idol = Idol(stage_name="Minyoung", real_name="Lee Minyoung", group=grupo)

    assert idol.real_name == "Lee Minyoung"
    assert grupo.company == "JYP"
    assert grupo.idols[0].stage_name == "Minyoung" 
    assert idol.group.name == "MIX6"

def test_database_validated():
    engine = create_engine('sqlite:///./api/idols.db')
    session = Session(bind=engine)
    
    grupo = Group(name="MIX6", company="JYP", id=100)
    idol = Idol(stage_name="Eunsuh", real_name="Lee Eunsuh", group=grupo)
    session.add(grupo)
    session.add(idol)
    session.commit()

    test_group = session.query(Group).options(joinedload(Group.idols)).filter(Group.id == 100).first()
    test_idol = session.query(Idol).options(joinedload(Idol.group)).filter(Idol.real_name == "Lee Eunsuh").first()
    assert test_group.name == "MIX6"
    assert test_group.idols[0].stage_name == "Eunsuh"
    assert test_idol.stage_name == "Eunsuh"
    assert test_idol.group.name == "MIX6"

    session.delete(idol)
    session.delete(grupo)
    session.commit()

    test_group = session.query(Group).options(joinedload(Group.idols)).filter(Group.id == 100).first()
    test_idol = session.query(Idol).options(joinedload(Idol.group)).filter(Idol.real_name == "Lee Eunsuh").first()

    assert test_group == None
    assert test_idol == None

    session.close()

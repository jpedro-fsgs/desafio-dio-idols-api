from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from api.schema import Idol, Group, get_session, Session
from api.models import IdolInput, GroupInput, IdolUpdate, GroupUpdate, IdolDelete, GroupDelete

app=FastAPI(title='IdolsAPI')

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://127.0.0.1:2130", "http://localhost:2130"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_group_id(name, session: Session = Depends(get_session)):
    group = session.query(Group).filter(func.lower(func.replace(Group.name, ' ', '')) == func.lower(name.replace(' ', ''))).first()
    if group: return group.id

@app.get('/')
async def root():
    return {"IdolsAPI": "아이돌에이피아이"}

@app.get('/groups')
async def get_groups(session: Session = Depends(get_session)):
    groups = session.query(Group).options(joinedload(Group.idols)).all()
    return groups

@app.get('/idols')
async def get_idols(session: Session = Depends(get_session)):
    idols = session.query(Idol).options(joinedload(Idol.group)).all()
    if idols: return idols
    raise HTTPException(status_code=404, detail='No Idols found')

@app.get('/group/{group_id_or_name}')
async def get_group(group_id_or_name: str, session: Session = Depends(get_session)):
    if group_id_or_name.isdigit():
        group_id_or_name = int(group_id_or_name)
    else:
        group_id_or_name = get_group_id(group_id_or_name, session=session)
    group = session.query(Group).options(joinedload(Group.idols)).filter(Group.id == group_id_or_name).first()
    if group: return group
    raise HTTPException(status_code=404, detail='Group not found')

@app.post("/idol")
async def register_idol(idol_input: IdolInput, session: Session = Depends(get_session)):
    if idol_input.group.isdigit():
        id_group = int(idol_input.group)
    else:
        id_group = get_group_id(idol_input.group, session=session)
    try:
        idol = Idol(stage_name=idol_input.stage_name, real_name=idol_input.real_name, group_id=id_group.id)
        session.add(idol)
        session.commit()
        return {"id": idol.id,
                "stage_name": idol.stage_name}
    except:
        raise HTTPException(status_code=404, detail='Group not found')

@app.post("/group")
async def register_group(group_input: GroupInput, session: Session = Depends(get_session)):
    try:
        group = Group(name=group_input.name, company=group_input.company)
        session.add(group)
        session.commit()
    except:
        raise HTTPException(status_code=409, detail='Group already added')
    for idol_input in group_input.idols:
        idol = Idol(stage_name=idol_input.stage_name, real_name=idol_input.real_name, group_id=group.id)
        session.add(idol)
    session.commit()
    return {"id": group.id,
            "name": group.name}

@app.put('/idol/')
async def update_idol(idol_update: IdolUpdate, session: Session = Depends(get_session)):
    idol = session.query(Idol).filter(Idol.id == idol_update.id).first()
    if idol:
        if idol_update.stage_name:
            idol.stage_name = idol_update.stage_name
        if idol_update.real_name:
            idol.real_name = idol_update.real_name
        if idol_update.group:
            idol.group_id = idol_update.group
        session.add(idol)
        session.commit()
        return {"id": idol.id,
                "stage_name": idol.stage_name}
    
    raise HTTPException(status_code=404, detail='Idol not found')

@app.put('/group/')
async def update_idol(group_update: GroupUpdate, session: Session = Depends(get_session)):
    group = session.query(Group).filter(Group.id == group_update.id).first()
    if group:
        if group_update.name:
            group.name = group_update.name
        if group_update.company:
            group.company = group_update.company
        session.add(group)
        session.commit()
        return {"id": group.id,
                "name": group.name}
    
    raise HTTPException(status_code=404, detail='Group not found')

@app.delete('/idol/')
async def delete_idol(idol_delete: IdolDelete, session: Session = Depends(get_session)):
    idol_query = session.query(Idol).filter(Idol.id == idol_delete.id)
    idol=idol_query.first()
    if idol:
        session.delete(idol)
        session.commit()
        return {"deleted": idol.stage_name}
    
    raise HTTPException(status_code=404, detail='Idol not found')

@app.delete('/group/')
async def delete_group(group_delete: GroupDelete, session: Session = Depends(get_session)):
   
   group = session.query(Group).filter(Group.id == group_delete.id).first()
   if group:
        for idol in group.idols:
            session.delete(idol)
        session.delete(group)
        session.commit()
        return {
            "group_deleted": group.name,
            "members_deleted": [idol.stage_name for idol in group.idols]
        }
   raise HTTPException(status_code=404, detail='Group not found')

''' Content resolver, provides the interaction with the database '''
from models import db

def get_or_create_it(model, model_info):
    ''' Returns the requested object from the database, if dont exists, the object is created '''
    instance_id = model_info['_id']
    instance = get(model=model, _id=instance_id).first()
    if not instance:
        instance = model(model_info)
    return instance

def get(model, **kwargs):
    ''' Returns the object for the params passed '''
    return db.session.query(model).filter_by(**kwargs)

def update(instance):
    ''' Updates the instance passed in the database '''
    db.session.add(instance)
    db.session.commit()

''' Content resolver, provides the interaction with the database '''
from models import db


class ContentResolverAbstract:
    ''' Abstract class for Content Resolvers '''
    def get_or_create_it(self, model, model_info):
        ''' Returns the requested object from the database,
        if dont exists, the object is created '''
        raise NotImplementedError

    def get(self, model, **kwargs):
        ''' Returns the object for the params passed '''
        raise NotImplementedError

    def update(self, instance):
        ''' Updates the instance passed in the database '''
        raise NotImplementedError

    def delete(self, instance):
        ''' Updates the instance passed in the database '''
        raise NotImplementedError


class StaticContentResolver(ContentResolverAbstract):
    ''' Simple Content Resolver '''
    def get_or_create_it(self, model, model_info):
        instance_id = model_info['_id']
        instance = self.get(model=model, _id=instance_id)
        if instance:
            created = False
            instance = self.get(model=model, _id=instance_id)[0]
        else:
            created = True
            instance = model(model_info)
        return instance, created

    def get(self, model, **kwargs):
        return db.session.query(model).filter_by(**kwargs).all()

    def update(self, instance):
        db.session.add(instance)
        db.session.commit()

    def delete(self, instance):
        ''' Updates the instance passed in the database '''
        db.session.delete(instance)
        db.session.commit()


content_resolver = StaticContentResolver()

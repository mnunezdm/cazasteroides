''' Content resolver, provides the interaction with the database '''
from sqlalchemy import inspect
import threading

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

class StaticContentResolver(ContentResolverAbstract):
    def __init__(self, db):
        self.db = db

    def get_or_create_it(self, model, model_info):
        instance_id = model_info['_id']
        instance = self.get(model=model, _id=instance_id)
        if instance:
            instance = self.get(model=model, _id=instance_id)[0]
        else:
            instance = model(model_info)
        return instance

    def get(self, model, **kwargs):
        return self.db.session.query(model).filter_by(**kwargs).all()

    def update(self, instance):
        self.db.session.add(instance)
        self.db.session.commit()

class ThreadedUpdateContentResolver(ContentResolverAbstract):
    def __init__(self, db):
        self.db = db

    def get_or_create_it(self, model, model_info):
        instance_id = model_info['_id']
        instance = self.get(model=model, _id=instance_id).first()
        if not instance:
            instance = model(model_info)
        return instance

    def get(self, model, **kwargs):
        return self.db.session.query(model).filter_by(**kwargs)

    def update(self, instance):
        session = inspect(instance).session
        updater = threading.Thread(target=self.__update_threaded, args=(session, instance))
        updater.start()

    @staticmethod
    def __update_threaded(session, instance):
        session.add(instance)
        session.commit()




class CachedContentResolver(StaticContentResolver):
    def __init__(self, app, db, model_observation, model_user):
        self.db = db
        self.model_observation = model_observation
        self.model_user = model_user
        with app.app_context():
            db.metadata.create_all(db.engine)
            self.observations = db.session.query(model_observation).all()
            self.users = db.session.query(model_user).all()


    def get_or_create_it(self, model, model_info):
        ''' Returns the requested object from the database,
        if dont exists, the object is created '''
        if self.model_observation == model:
            return self.__get_or_create_observation(model_info)
        if self.model_user == model:
            return self.__get_or_create_user(model_info)
        else:
            return super(CachedContentResolver, self).get_or_create_it(model, model_info)

    def __get_or_create_observation(self, model_info):
        observation = self.__get_observation_by_id(model_info['_id'])
        if not observation:
            print('observation creado')
            observation = self.model_observation(model_info)
        self.observations.append(observation)
        return observation

    def __get_observation_by_id(self, _id):
        observations = [observation for observation in self.observations if observation == _id]
        if observations:
            return observations[0]

    def __get_or_create_user(self, model_info):
        user = self.__get_user_by_id(model_info['_id'])
        if not user:
            print('usuario creado')
            user = self.model_user(model_info)
        self.users.append(user)
        return user

    def __get_user_by_id(self, _id):
        users = [user for user in self.users if user == _id]
        if users:
            return users[0]

    def update(self, instance):
        ''' Updates the instance passed in the database '''
        self.db.session.add(instance)
        self.db.session.commit()

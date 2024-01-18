from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


user_task = db.Table('user_task',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('task_id',db.Integer,db.ForeignKey('task.id'))

)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    name = name = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = name = db.Column(db.String(255))
    data = db.Column(db.String(1000000))
    output = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    request_limit = db.Column(db.Integer)
    request_limit_is_reached = db.Column(db.Boolean)
    is_done = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    logs = db.relationship('Logs')
    
# class Reminder(db.Model):

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(10000))   
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    codes = db.relationship('Code')
    request_limit = db.Column(db.Integer)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    # Users = db.relationship('U',secondary=user_task,backref='tasks')
    
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    codes = db.relationship('Code')
    requests = db.relationship('Request',foreign_keys="[Request.requester_id]")
    requested = db.relationship('Request',foreign_keys="[Request.requestee_id]")
    accepted = db.relationship('Approved',foreign_keys="[Approved.requester_id]")
    accepts = db.relationship('Approved',foreign_keys="[Approved.acceptor_id]")
    request_limit = db.Column(db.Integer)
    request_limit_is_reached = db.Column(db.Boolean)

    Tasks = db.relationship('Task',secondary=user_task,backref='users')
    is_admin = db.Column(db.Boolean)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note')
    # codes = db.relationship('Code')
    # Tasks = db.relationship('Task',secondary=user_task,backref='users')
    tasks = db.relationship('Task')
    students = db.relationship('User')
    rooms = db.relationship('Room')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    data = db.Column(db.String(10000))   
    name = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requestee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
   
    rooms = db.relationship('Room')
    logs = db.relationship('Logs')
    requester_name = db.Column(db.String(255))



class Approved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    data = db.Column(db.String(10000))   
    name = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    acceptor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))



class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    helper_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    request_id  = db.Column(db.Integer, db.ForeignKey('request.id'))
    requester_name = db.Column(db.String(255))
    helper_name = db.Column(db.String(255))



class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    before = db.Column(db.String(1000000))
    after = db.Column(db.String(1000000))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
    helper_name = db.Column(db.String(255))
    error_type = db.Column(db.String(255))
    output = db.Column(db.String(10000))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
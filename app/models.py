from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Committee(db.Model):
    __tablename__ = 'committees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('committees.id'), nullable=True)
    parent = db.relationship('Committee', remote_side=[id], backref=db.backref('sub_committees', lazy=True))

    __table_args__ = (
        UniqueConstraint('parent_id', 'name', name='uix_parent_name'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'parent_id': self.parent_id,
            'sub_committees': [sub.to_dict() for sub in self.sub_committees]
        }


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.id'))
    committee = db.relationship('Committee', backref=db.backref('persons', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'committee': self.committee.to_dict() if self.committee else None
        }


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


def create_admin_user():
    admin = Admin.query.filter_by(name='admin').first()
    if not admin:
        new_admin = Admin(name='admin', password=generate_password_hash('password', method='sha256'))
        db.session.add(new_admin)
        db.session.commit()


class Iogv(db.Model):
    __tablename__ = 'iogv'
    hierarchy_id = db.Column(db.String, primary_key=True)
    depth_level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.String, db.ForeignKey('iogv.hierarchy_id'), nullable=True)
    parent = db.relationship('Iogv', remote_side=[hierarchy_id], backref=db.backref('sub_iogvs', lazy=True))

    def to_dict(self):
        return {
            'hierarchy_id': self.hierarchy_id,
            'depth_level': self.depth_level,
            'name': self.name,
            'parent_id': self.parent_id,
            'sub_iogvs': [sub.to_dict() for sub in self.sub_iogvs]
        }


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.Text, nullable=False)
    iogv_id = db.Column(db.String, db.ForeignKey('iogv.hierarchy_id'), nullable=True)
    subdivision_id = db.Column(db.String, db.ForeignKey('iogv.hierarchy_id'), nullable=True)
    person_id = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=False)
    iogv = db.relationship('Iogv', foreign_keys=[iogv_id], backref=db.backref('users', lazy=True))
    subdivision = db.relationship('Iogv', foreign_keys=[subdivision_id],
                                  backref=db.backref('subdivision_users', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post,
            'iogv_id': self.iogv_id,
            'subdivision_id': self.subdivision_id,
            'person_id': self.person_id,
            'created_at': self.created_at,
            'iogv': self.iogv.to_dict() if self.iogv else None,
            'subdivision': self.subdivision.to_dict() if self.subdivision else None
        }


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    responce_time = db.Column(db.String, nullable=True)
    created_at = db.Column(db.String, nullable=False)
    user = db.relationship('User', backref=db.backref('records', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'responce_time': self.responce_time,
            'created_at': self.created_at,
            'user': self.user.to_dict() if self.user else None
        }


class Answer(db.Model):
    __tablename__ = 'answers'
    rid = db.Column(db.Integer, db.ForeignKey('record.id'), primary_key=True)
    number_question = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String, nullable=True)
    record = db.relationship('Record', backref=db.backref('answers', lazy=True))

    def to_dict(self):
        return {
            'rid': self.rid,
            'number_question': self.number_question,
            'answer': self.answer,
            'comment': self.comment,
            'record': self.record.to_dict() if self.record else None
        }


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iogv = db.Column(db.String, nullable=False)
    subdv = db.Column(db.String, nullable=False)
    post = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id', ondelete='CASCADE'))
    record = db.relationship('Record', backref=db.backref('reports', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'iogv': self.iogv,
            'subdv': self.subdv,
            'post': self.post,
            'created_at': self.created_at,
            'link': self.link,
            'record_id': self.record_id,
            'record': self.record.to_dict() if self.record else None
        }


class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }


class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone': self.phone
        }


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.String, unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'value': self.value
        }


class Direction(db.Model):
    __tablename__ = 'directions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    criterions = db.relationship('Criterion', backref='direction', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'criterions': [criterion.to_dict() for criterion in self.criterions]
        }


class Criterion(db.Model):
    __tablename__ = 'criterions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    direction_id = db.Column(db.Integer, db.ForeignKey('directions.id'), nullable=False)
    subcriterions = db.relationship('Subcriterion', backref='criterion', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'number': self.number,
            'subcriterions': [subcriterion.to_dict() for subcriterion in self.subcriterions]
        }


class Subcriterion(db.Model):
    __tablename__ = 'subcriterions'
    id = db.Column(db.Integer, primary_key=True)
    question_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    criterion_id = db.Column(db.Integer, db.ForeignKey('criterions.id'), nullable=False)
    needed_answer = db.Column(db.Boolean, default=False, nullable=False)
    puncts = db.relationship('Punct', backref='subcriterion', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question_number': self.question_number,
            'title': self.title,
            'weight': self.weight,
            'needed_answer': self.needed_answer,
            'puncts': [punct.to_dict() for punct in self.puncts]
        }


class Punct(db.Model):
    __tablename__ = 'puncts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    prompt = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    subcriterion_id = db.Column(db.Integer, db.ForeignKey('subcriterions.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'range_min': self.range_min,
            'range_max': self.range_max,
            'prompt': self.prompt,
            'comment': self.comment
        }

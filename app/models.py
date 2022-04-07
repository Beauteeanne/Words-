from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)   
    phone = db.Column(db.String(), nullable=False)
    image = db.Column(db.Text, nullable=True)
    cv = db.Column(db.Integer, nullable=True)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, first_name, last_name, email, phone, password, image, cv):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.image = image
        self.cv = cv

    def __repr__(self):
        return '<name {}>'.format(self.first_name)

    def is_Admin(self, user):
        """Does this user have this permission?"""
        is_Admin = Admins.query.filter_by(user=user).first()
        if is_Admin:
            return True
        else:
            return False

class Admins(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref="users", foreign_keys=user_id)
    # backpopulate uselist
    active = db.Column(db.Boolean(), default=False,nullable=False)

    def __init__(self, user_id, active):
        self.user_id = user_id
        self.active = active

    def __repr__(self):
        return '<id {}>'.format(self.id)


class  Cv(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'cv'

    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref="user_cv", foreign_keys=user_id)
    cv = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, cv, mimetype, user):
        self.cv = cv
        self.mimetype = mimetype
        self.user = user

    def __repr__(self):
        return 'id {}'.format(self.id)          


class Job(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(), nullable=True)

    # foriegn keys
    category_id = db.Column(db.Integer, db.ForeignKey('job_category.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accepted_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # relationships
    category = db.relationship('Job_Category', backref="job_category", foreign_keys=category_id)
    owner = db.relationship("User", backref="owner", foreign_keys=created_by_id)
    freelancer = db.relationship("User", backref="freelancer", foreign_keys=created_by_id, overlaps='owner, owner')
    
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, description, title, image, price, owner, freelancer, category):
        self.description = description
        self.title = title
        self.image = image
        self.price = price
        self.owner = owner
        self.freelancer = freelancer
        self.category = category
        # .join(Job_Category)

    def __repr__(self):
        return '<id {}>'.format(self.id)



class Job_Category(db.Model):
    __table_args__ = {'extend_existing': True} 
    __tablename__ = 'job_category'

    id = db.Column(db.Integer, autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, description=description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)
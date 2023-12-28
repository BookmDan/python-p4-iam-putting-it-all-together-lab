from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # Add this line for the primary key
    username = Column(String)
    _password_hash = Column(String)
    image_url = Column(String)
    bio = Column(String)

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    recipes = relationship('Recipe', backref='user', lazy=True)

    def __repr__(self):
        return f'User ID: {self.id}, Username: {self.username}'
    
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    table= Column(String, nullable=False)
    instructions = Column(String, nullable = False, length=50)
    minutes_to_complete= Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # other columns for the Recipe model...

    def __repr__(self):
        return f'Recipe ID: {self.id}, ...'
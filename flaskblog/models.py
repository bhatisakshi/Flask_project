from .db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
        
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }
        
    def __repr__(self):
        return f'<BlogPost {self.title}>'

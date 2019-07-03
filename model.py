from scrap import db
from sqlalchemy import Column, Integer, Text

class CRUD():
     def save(self):
         if self.id == None:
             db.session.add(self)
         return db.session.commit()

class Car(db.Model, CRUD):
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    name = Column(Text, unique=True)
    desciption = Column(Text)
    def  __repr__(self):
        return '<Car %r>' % self.name
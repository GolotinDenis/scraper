
from sqlalchemy import Column, Integer, Text

from scrap import db


class Car(db.Model):
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    name = Column(Text)
    desciption = Column(Text)
    model = Column(Text)

    def save(self):
         if self.id == None:
             db.session.add(self)
         return db.session.commit()

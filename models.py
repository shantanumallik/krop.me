from app import db
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import JSON

class Uap(db.Model):
    __tablename__ = 'url_map'

    short_url = db.Column(db.String(50), primary_key=True)
    long_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime())
    expiry = db.Column(db.Integer())
    visit_count = db.Column(db.Integer())	

    def __init__(self,short_url, long_url, created_at, expiry, visit_count):
        self.short_url = short_url
        self.long_url = long_url
        self.created_at = datetime.now()
        self.expiry = int(date.today().year) + 3
        self.visit_count = 0

    def __repr__(self):
        return '<short_url {}>'.format(self.short_url)
    
    def serialize(self):
        return {
            'short_url': self.short_url, 
            'long_url': self.long_url,
            'created_at': self.created_at,
            'expiry':self.expiry,
            'visit_count':self.visit_count		
        }

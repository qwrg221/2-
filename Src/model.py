from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    image_data = db.Column(db.LargeBinary)
    size = db.Column(db.Integer)
    resolution = db.Column(db.String(20))
    date_created = db.Column(db.String(20))
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CountryInfoDto(db.Model):
    __tablename__ = 'CountryInfo'
    CountryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CountryName = db.Column(db.String(100))
    CapitalState = db.Column(db.String(100))
    NationalBird = db.Column(db.String(100))
    CountryPopulation = db.Column(db.BigInteger)

#!/usr/bin/python3
'''
    Define the class Place.
'''
# from models.engine import storage
from models.review import Review
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


class PlaceAmenity(Base):
    __tablename__ = "place_amenity"
    place_id = Column(String(60),
                      ForeignKey("places.id"),
                      primary_key=True,
                      nullable=False),
    amenity_id = Column(String(60),
                        ForeignKey("amenities.id"),
                        primary_key=True,
                        nullable=False)
    metadata = Base.metadata


class Place(BaseModel, Base):
    '''
        Define the class Place that inherits from BaseModel.
    '''
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name  = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place', cascade='delete')
        amenities = relationship('Amenity', secondary="place_amenity", viewonly=False)
    else:
        @property
        def reviews(self):
            obj_dict = storage.all(Review)
            for key, value in obj_dict:
                if value.place_id is not self.id:
                    del obj_dict[key]
            return obj_dict

        @property
        def amenities(self):
            obj_dict = storage.all(Amenity)
            for key, value in obj_dict:
                if value.place_id is not self.id:
                    del obj_dict[key]
            return obj_dict

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'

    station_id = Column(Integer, primary_key=True, autoincrement=True)
    station_name = Column(String, nullable=False)

    start_rentals = relationship("Rental", back_populates="start_station", foreign_keys='Rental.rental_station')
    end_rentals = relationship("Rental", back_populates="end_station", foreign_keys='Rental.return_station')


class Rental(Base):
    __tablename__ = 'rentals'

    rental_id = Column(String, primary_key=True)
    bike_number = Column(String, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)

    rental_station = Column(Integer, ForeignKey('stations.station_id'), nullable=True)
    return_station = Column(Integer, ForeignKey('stations.station_id'), nullable=True)

    start_station = relationship("Station", foreign_keys=[rental_station], back_populates="start_rentals")
    end_station = relationship("Station", foreign_keys=[return_station], back_populates="end_rentals")

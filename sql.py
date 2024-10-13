from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship, sessionmaker

username = 'postgres'
password = '123'
host = '127.0.0.1'
port = '5432'
database = 'sri'


connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

Base = declarative_base()
metadata = Base.metadata

grn_table = Table('grn', metadata , Column('grn_no', Integer, primary_key=True), autoload_with=engine)

class GRN(Base):
    __table__ = grn_table

    alerts = relationship("Alerts", back_populates="grn")

#mapper(GRN, grn)

class Alerts(Base):
    __tablename__ = 'alerts'
    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Correct ForeignKey reference to GRN vehicle_number
    grn_no = Column(String, ForeignKey("grn.grn_no"))
    
    # Relationship with GRN, back_populates must match 'alerts' in GRN
    grn = relationship('GRN', back_populates='alerts')  
    
    alert_type = Column(String(50))
    timestamp = Column(DateTime)
    # Polymorphic configuration
    __mapper_args__ = {
        'polymorphic_on': alert_type,
        'polymorphic_identity': 'alert'
    }


class Overspeeding(Alerts):
    __tablename__ = 'speeding'
    
    # Inheriting alert_id from Alerts and setting it as a ForeignKey
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'), primary_key=True)  
    
    duration = Column(Integer)
    distance_covered = Column(Float)

    # Setting the polymorphic identity for this class
    __mapper_args__ = {
        'polymorphic_identity': 'Overspeeding' 
    }
class Idling(Alerts):
    __tablename__ = 'idling'
    
    # Inheriting alert_id from Alerts and setting it as a ForeignKey
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'), primary_key=True)  
    
    duration = Column(Integer)

    # Setting the polymorphic identity for this class
    __mapper_args__ = {
        'polymorphic_identity': 'idling'
    }
class Hard_brake(Alerts):
    __tablename__ = 'hard_brake'
    alert_id = Column(Integer, ForeignKey("alerts.alert_id"), primary_key=True )
    duration = Column(Integer)

    __mapper_args__ = {
            'polymorphic_identity' : 'hard_brake'
        }

class Freerun(Alerts):
    __tablename__ = 'freerun'
    alert_id = Column(Integer, ForeignKey('alerts.alert_id'), primary_key=True)
    distance = Column(Integer)
    max_speed = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity' : 'freerun'
    }

Base.metadata.create_all(engine)

if __name__ == '__main__':
    print('all ok')

import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Hazard(SqlAlchemyBase):
    __tablename__ = 'hazards'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    jobs = orm.relationship('Jobs', back_populates='hazard')

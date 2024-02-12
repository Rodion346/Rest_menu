import uuid

from sqlalchemy import DECIMAL, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(150), nullable=False)
    description = Column(String(500))
    manual_id = Column(String, unique=True, nullable=True)

    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(150), nullable=False)
    description = Column(String(500))
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    manual_id = Column(String, unique=True, nullable=True)

    menu = relationship('Menu', back_populates='submenus', single_parent=True)
    dishes = relationship('Dishes', back_populates='submenu', cascade='all, delete-orphan')


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(150), nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    description = Column(String(500))
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    manual_id = Column(String, unique=True, nullable=True)

    submenu = relationship('Submenu', back_populates='dishes', single_parent=True)

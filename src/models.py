import uuid
from sqlalchemy import String, Column, MetaData, ForeignKey, DECIMAL, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

metadata = MetaData()


class Menu(Base):
    __tablename__ = "menus"

    metadata = metadata
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(60), nullable=False)
    description = Column(String(125))

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")


class Submenu(Base):
    __tablename__ = "submenus"

    metadata = metadata
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False)
    description = Column(String(125))
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus", single_parent=True)
    dishes = relationship("Dishes", back_populates="submenu", cascade="all, delete-orphan")


class Dishes(Base):
    __tablename__ = "dishes"
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False)
    price = Column(DECIMAL, nullable=False)
    description = Column(String(125))
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes", cascade="all, delete-orphan", single_parent=True)
import uuid
from sqlalchemy import String, Column, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.database import Base

class Menu(Base):
    __tablename__ = "menus"
    id: UUID(as_uuid=True) = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: String(50) = Column(String(50), nullable=False)
    description: String(125) = Column(String(125))

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")

class Submenu(Base):
    __tablename__ = "submenus"
    id: UUID(as_uuid=True) = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: String(50) = Column(String(50), nullable=False)
    description: String(125) = Column(String(125))
    menu_id: UUID(as_uuid=True) = Column(UUID(as_uuid=True), ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus", single_parent=True)
    dishes = relationship("Dishes", back_populates="submenu", cascade="all, delete-orphan")

class Dishes(Base):
    __tablename__ = "dishes"
    id: UUID(as_uuid=True) = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: String(50) = Column(String(50), nullable=False)
    price: DECIMAL = Column(DECIMAL, nullable=False)
    description: String(125) = Column(String(125))
    submenu_id: UUID(as_uuid=True) = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes", cascade="all, delete-orphan", single_parent=True)
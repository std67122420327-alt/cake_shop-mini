from foodapp.extensions import db, login_manager
from sqlalchemy import Integer, Text, String, Boolean, DateTime, ForeignKey, Column, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  firstname: Mapped[str] = mapped_column(String(25), nullable=True)
  lastname: Mapped[str] = mapped_column(String(25), nullable=True)
  avatar: Mapped[str] = mapped_column(String(25), nullable=True, default='avatar.png')
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  foods: Mapped[List['Food']] = relationship(back_populates='user')
  def __repr__(self):
    return f'<User: {self.username}>'

food_categories = Table(
  'food_categories',
  db.metadata,
  Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
  Column('food_id', Integer, ForeignKey('food.id'), primary_key=True)
)

class Category(db.Model):
  __tablename__ = 'category'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

  foods: Mapped[List['Food']] = relationship(back_populates='categories', secondary=food_categories)
  def __repr__(self):
    return f'<Category: {self.name}>'
  
class Food(db.Model):
  __tablename__ = 'food'
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  price: Mapped[str] = mapped_column(String(25), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  img_url: Mapped[str] = mapped_column(String(255), nullable=False)
  is_available: Mapped[bool] = mapped_column(Boolean, default=True)
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

  user: Mapped[User] = relationship(back_populates='foods')
  categories: Mapped[List[Category]] = relationship(back_populates='foods', secondary=food_categories)
  
  def __repr__(self):
    return f'<Food: {self.name}>'
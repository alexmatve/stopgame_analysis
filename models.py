from datetime import datetime

from sqlalchemy.orm import sessionmaker, relationship, declarative_base, mapped_column, Mapped
from sqlalchemy import Table, Column, create_engine, Integer, String, Float, Date
import os
from typing import Optional
from sqlalchemy import ForeignKey

# self.title = str()
#         self.rating = float()
#         self.release = str()
#         self.sites = list()
#         self.developer = list()
#         self.publisher = list()
#         self.platforms = list()
#         self.href = str()
#         self.editorial_rating = str()

class GameORM:
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column()
    release: Mapped[str] = mapped_column()
    href: Mapped[str] = mapped_column()
    editorial_rating: Mapped[float] = mapped_column(nullable=True)
    site:  Mapped[int] = mapped_column(ForeignKey("sites.id"))
    developer:  Mapped[int] = mapped_column(ForeignKey("developers.id"))
    publisher:  Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    platform:  Mapped[int] = mapped_column(ForeignKey("platforms.id"))

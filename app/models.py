from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(16))
    name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    habilitado: Mapped[bool] = mapped_column(default=True, server_default="1")

    posts: Mapped[list["Post"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64))
    body: Mapped[str]
    usuario_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
    categories: Mapped[list["Category"]] = relationship(
        back_populates="posts", secondary="posts_categories"
    )
    image: Mapped["Image"] = relationship(back_populates="post", uselist=False)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))

    posts: Mapped[list["Post"]] = relationship(
        back_populates="categories", secondary="posts_categories"
    )


class PostCategory(Base):
    __tablename__ = "posts_categories"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(64))
    url: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), unique=True)

    post: Mapped["Post"] = relationship(back_populates="image")

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.models import Category, Post, User

engine = create_engine("sqlite:///db.sqlite3", echo=False)
Session = sessionmaker(engine)


def main():
    crear_datos()


def consultar_datos():
    with Session() as session:
        usuario = session.execute(select(User)).scalars().first()
        if usuario is not None:
            print(usuario.id, usuario.username)

            print(usuario.posts[0].user)


def modificar_datos():
    with Session() as session:
        usuario2 = session.get(User, 2)
        print(usuario2)
        stmt = select(Post).where(Post.title == "Mi segundo post")
        post2 = session.execute(stmt).scalar_one()
        post2.user = usuario2
        session.commit()


def crear_datos():
    with Session() as session:
        c1 = Category(name="Informaciones")
        c2 = Category(name="General")
        p1 = Post(title="Mi primer post", body="Este es mi primer post. Blabla", categories=[c1])
        p2 = Post(
            title="Mi segundo post", body="Este es mi segundo post. Blabla", categories=[c1, c2]
        )
        u1 = User(username="user1", name="User 1", posts=[p1, p2])
        u2 = User(username="user2", name="User 2")

        session.add_all([c1, c2, p1, p2, u1, u2])
        session.commit()


if __name__ == "__main__":
    main()

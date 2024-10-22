from graphQL_app.model.models import engine, db_session, Base, User, Blog, Post



Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# Введём тестовые данные

user1 = User(name='User1 name', email="user1@mail.ru", password="qwerty123")
db_session.add(user1)

user2 = User(name='User2 name', email="user2@gmail.com", password="qwerty23")
db_session.add(user2)

user3 = User(name='User3 name', email="user3@mailbox.org", password="qwerty321")
db_session.add(user3)




blog1 = Blog(owner=user1, name='User 1 blog')
db_session.add(blog1)

blog2 = Blog(owner=user1, name='User 1 second blog')
db_session.add(blog2)



post1 = Post(blog=blog1, title="Post in User 1's first blog", text="Lorum Ipsum")
db_session.add(post1)

db_session.commit()

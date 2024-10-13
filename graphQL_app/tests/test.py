from graphQL_app.model.models import engine, db_session, Base, User, Blog, Post


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# Введём тестовые данные
user1 = User(user_id=1, user_name='User1 name')
db_session.add(user1)

user2 = User(user_id=2, user_name='User2 name')
db_session.add(user2)

blog1 = Blog(owner_id=1, blog_id=1, blog_name='User 1 blog')
db_session.add(blog1)

blog2 = Blog(owner_id=1, blog_name='User 1 second blog')
db_session.add(blog2)


user3 = User(user_id=3, user_name='User3 name')
db_session.add(user3)

post1 = Post(blog_id = 1, title= "Post in User 1's first blog", text="Lorum Ipsum")
db_session.add(post1)


db_session.commit()
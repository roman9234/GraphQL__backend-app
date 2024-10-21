GraphQL обеспечивает гибкий API и убирает необходимость постоянно писать новые запросы

Документация

Запросы - делаются через оператор query. Аналог GET запросов в REST

Мутации - аналог POST или PUT запросов в REST.
В мутациях также указываем поля, которые вернутся по результату запроса

Подписки - получаем в реальном времени все обновления и изменения.







Конвертер GraphQL - query в одну строчку:
https://datafetcher.com/graphql-json-body-converter


---- ---- ----
Шаблон запросов для Curl:

curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query="

---- ---- ----


---- Аутентификация

mutation {
  authentication(email: "user1@mail.ru", password: "qwerty123") {
    accessToken
  }
}


---- Получение списка пользователей и каждого блога пользователя:
curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query={ allUsers { edges { node { name blogs { edges { node { name } } } } } }}"

{
  allUsers {
    edges {
      node {
        name
        blogs {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}

---- Получение пользователя по имени, вывод всех его блогов и всех постов:
curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query={ getUser(id: 1) { name blogs { edges { node { name posts { edges { node { title text } } } } } } }}"

{
  getUser(id: 1) {
    name
    blogs {
      edges {
        node {
          name
          posts {
            edges {
              node {
                title
                text
              }
            }
          }
        }
      }
    }
  }
}

---- Добавление нового пользователя

curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query=mutation { createUser(name: \"User new\", email: \"userNew@gmail.com\",password: \"qwerty\") { user { id name } }}"

mutation {
  createUser(name: "User new", email: "userNew@gmail.com",password: "qwerty") {
    user {
      id
      name
    }
  }
}

---- Обновление данных пользователя
Можно менять несколько полей сразу, или например только одно
Зависит от аргументов

curl -d "query=mutation { updateUser(id: 1, name: \"User1 new name\"){ user{ name id } }}" -L "http://127.0.0.1:5000/graphql/" -XPOST


mutation {
  updateUser(id: 1, name: "User1 new name", accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJ1c2VyMUBtYWlsLnJ1IiwiZXhwaXJhdGlvbiI6IjIwMjQtMTAtMjIgMjI6MTI6MDAifQ.whe8krQexNFlsKfNGVExe-qfvOL_vRgt2zJQUw9XLY4") {
    user {
      email
      name
      id
    }
  }
}

---- Создание нового блога

mutation {
  createBlog(userId: 2, name: "User 2 new blog", accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJ1c2VyMkBnbWFpbC5jb20iLCJleHBpcmF0aW9uIjoiMjAyNC0xMC0yMiAyMjoxMjowMyJ9.GIKL9k1jCXY_n_ebG2scxvIP1eD3tNCSt80nDQErAsA"){
    blog{
      name
      owner{
        name
      }
    }
  }
}


---- Обновление данных блога

mutation{
  updateBlog(blogId: 2, name: "even newer User 2 blog", accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJ1c2VyMkBnbWFpbC5jb20iLCJleHBpcmF0aW9uIjoiMjAyNC0xMC0yMiAyMjoxMjowMyJ9.GIKL9k1jCXY_n_ebG2scxvIP1eD3tNCSt80nDQErAsA"){
    blog{
      name
      owner{
        name
      }
    }
  }
}

---- Создание нового поста в блоге

mutation {
  createPost(blogId: 3, text: "hello, this first post in my new blog!", title: "First post in my new blog", accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJ1c2VyMkBnbWFpbC5jb20iLCJleHBpcmF0aW9uIjoiMjAyNC0xMC0yMiAyMjoxMjowMyJ9.GIKL9k1jCXY_n_ebG2scxvIP1eD3tNCSt80nDQErAsA") {
    post {
      title
      text
    }
  }
}

---- Изменение поста в блоге

mutation {
  updatePost(id: 3, text: "Hello, this is my new blog! Soon there will be even more posts!!!", accessToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJ1c2VyMkBnbWFpbC5jb20iLCJleHBpcmF0aW9uIjoiMjAyNC0xMC0yMiAyMjoxMjowMyJ9.GIKL9k1jCXY_n_ebG2scxvIP1eD3tNCSt80nDQErAsA") {
    post {
      title
      text
    }
  }
}












Источники:

Авторизация в таком приложении с использованием Auth0
https://auth0.com/blog/dynamic-authorization-with-graphql-and-rules/

Авторизация через токены
https://qxf2.com/blog/graphql-flask-jwt-sqlalchemy/


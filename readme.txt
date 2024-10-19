GraphQL обеспечивает гибкий API и убирает необходимость постоянно писать новые запросы

Документация

Запросы - делаются через оператор query. Аналог GET запросов в REST

Мутации - аналог POST или PUT запросов в REST.
В мутациях также указываем поля, которые вернутся по результату запроса

Подписка - получаем в реальном времени все обновления и изменения.







Конвертер GraphQL - query в одну строчку:
https://datafetcher.com/graphql-json-body-converter


---- ---- ----
Шаблон запросов для Curl:

curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query="

---- ---- ----
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
curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query={ getUser(name: \"User1 name\") { name blogs { edges { node { name posts { edges { node { title text } } } } } } }}"

{
  getUser(name: "User1 name") {
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

curl -L "http://127.0.0.1:5000/graphql/" -XPOST -d "query=mutation { createUser(name: \"User new\") { user { id name } }}"

mutation {
  createUser(name: "User new") {
    user {
      id
      name
    }
  }
}

---- Обновление данных пользователя

curl -d "query=mutation { updateUser(id: 1, name: \"User1 new name\"){ user{ name id } }}" -L "http://127.0.0.1:5000/graphql/" -XPOST


mutation {
  updateUser(id: 1, name: "User1 new name"){
   user{
    name
    id
  }
  }
}

---- Создание нового блога

mutation {
  createBlog(userId: 2, name: "New User 2 blog"){
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
  updateBlog(blogId: 2, name: "even newer User 2 blog"){
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
  createPost(blogId: 2, text: "hello, this is my new blog!", title: "First post in my new blog") {
    post {
      title
      text
    }
  }
}

---- Изменение поста в блоге

mutation {
  updatePost(id: 2, text: "Hello, this is my new blog! Soon there will be even more posts!!!") {
    post {
      title
      text
    }
  }
}


Источники:
Авторизация в таком приложении с использованием Auth0
https://auth0.com/blog/dynamic-authorization-with-graphql-and-rules/



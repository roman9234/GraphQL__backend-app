GraphQL обеспечивает гибкий API и убирает необходимость постоянно писать новые запросы

Получение списка пользователей и каждого блога пользователя:
curl -L "http://127.0.0.1:5000/graphql/" -XGET -d "query={ allUsers { edges { node { userId userName blogs{ edges{ node{ blogId ownerId blogName } } } } } }}"

{
  allUsers {
    edges {
      node {
        userId
        userName
        blogs{
          edges{
            node{
              blogId
              ownerId
              blogName
            }
          }
        }
      }
    }
  }
}

Конвертер GraphQL - query в одну строчку:
https://datafetcher.com/graphql-json-body-converter

curl -L "http://127.0.0.1:5000/graphql/" -XGET -d "query={ allUsers { edges { node { userId userName blogs{ edges{ node{ blogId ownerId blogName posts{ edges{ node{ title text } } } } } } } } }}"



{
  allUsers {
    edges {
      node {
        userId
        userName
        blogs{
          edges{
            node{
              blogId
              ownerId
              blogName
              posts{
                edges{
                  node{
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
  }
}







GraphQL обеспечивает гибкий API и убирает необходимость постоянно писать новые запросы

Добавление книг:
curl -L "http://127.0.0.1:5000/graphql/" -XGET -d "query={ allEmployees { edges { node { id name department { name } } } } }"


{
  allEmployees {
    edges {
      node {
        id
        name
        department {
          name
        }
      }
    }
  }
}











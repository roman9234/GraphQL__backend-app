GraphQL обеспечивает гибкий API и убирает необходимость постоянно писать новые запросы


Attribute-Based Access Control (ABAC)

ABAC — это модель контроля доступа, основанная на атрибутах. Здесь решения о доступе принимаются на основе набора атрибутов,
которые могут быть связаны с пользователем, ресурсом, действием или окружением

1. Атрибуты: Это ключевые характеристики или свойства, например:
   • Пользовательские атрибуты: роль, отдел, возраст.
   • Атрибуты ресурса: тип документа, уровень конфиденциальности.
   • Атрибуты действия: чтение, запись, удаление.
   • Атрибуты окружения: время суток, местоположение.
2. Политики: Правила, которые определяют, какие атрибуты должны быть выполнены для разрешения доступа.
3. Принятие решения: Когда пользователь запрашивает доступ к ресурсу, система проверяет его атрибуты и сравнивает их с политиками,
чтобы принять решение о предоставлении или отказе в доступе.









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







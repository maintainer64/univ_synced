# Синхронизация двух систем

**Документация [к системам для сихронизации](https://github.com/maintainer64/univ_synced/tree/main/univdoc)**


### Потоки, диаграммы взаимодействия

#### Первичная синхронихация (из Multi в Single):

![GitHub Svg1](/univdoc/1.svg)

#### Первичная синхронихация (из Single в Multi):

![GitHub Svg2](/univdoc/2.svg)

#### Пример диаграммы непрерывной синхронизации сервисов:

![GitHub Svg3](/univdoc/3.svg)

В схеме:
 - N - Nginx (ApiGetaway-proxy)
 - App - Приложение для синхронизации
 - User - пользовательский запрос (внешний)
 - SingleCore, MultiCore - сервисы для синхронизации

### Схема, архитектура

#### Архитектура до синхронизатора:

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gICAgU2luZ2xlLUNvcmUtRG9tYWluIC0tPiBTaW5nbGUtQ29yZTtcbiAgICBNdWx0aS1Db3JlLURvbWFpbiAtLT4gTXVsdGktQ29yZTsiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gICAgU2luZ2xlLUNvcmUtRG9tYWluIC0tPiBTaW5nbGUtQ29yZTtcbiAgICBNdWx0aS1Db3JlLURvbWFpbiAtLT4gTXVsdGktQ29yZTsiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

#### Схема после:

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gICAgU2luZ2xlLUNvcmUtRG9tYWluIC0tPiBOZ2lueDtcbiAgICBNdWx0aS1Db3JlLURvbWFpbiAtLT4gTmdpbng7XG4gICAgTmdpbngtLT5BcHA7XG4gICAgQXBwLS0-U2luZ2xlLUNvcmU7XG4gICAgQXBwLS0-TXVsdGktQ29yZTtcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVEQ7XG4gICAgU2luZ2xlLUNvcmUtRG9tYWluIC0tPiBOZ2lueDtcbiAgICBNdWx0aS1Db3JlLURvbWFpbiAtLT4gTmdpbng7XG4gICAgTmdpbngtLT5BcHA7XG4gICAgQXBwLS0-U2luZ2xlLUNvcmU7XG4gICAgQXBwLS0-TXVsdGktQ29yZTtcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

# Library Manager CLI

**Library Manager CLI** — это командный интерфейс для управления библиотекой
книг. Проект позволяет добавлять, удалять, обновлять и просматривать книги, а
также искать их по названию или другим критериям. Все данные сохраняются в
формате JSON для обеспечения простоты работы и сохранения информации между
сессиями.

## Основные возможности

- **Добавление книг**:
    - Возможность добавления книги с указанием названия, автора, года издания и
      статуса (например, "в наличии" или "выдана").
    - Проверка на наличие обязательных параметров.
    - Проверка на пустоту значений
    - Проверка на соответствие типов
    - Проверка на "реальность" введённых значений

- **Просмотр книг**:
    - Отображение всех книг в виде таблицы с
      колонками: `ID`, `Название`, `Автор`, `Год издания`, `Статус`.
    - Поддержка фильтрации книг по ключевым словам.
  ```bash
  ID                                   | TITLE                  | AUTHOR              | YEAR | STATUS   
  ------------------------------------------------------------------------------------------------------
  f3f886a5-28fa-4e66-83d1-5731e5dd74cd | Сказка о золотой рыбке | А.С.Пушкин          | 1810 | выдана   
  7959c770-b0b1-4d86-b8f4-476310b465d6 | 1984                   | George Orwell       | 1949 | в наличии
 
  ```

- **Обновление статуса книги**:
    - Изменение статуса книги (например, с "в наличии" на "выдана").

- **Удаление книги**:
    - Удаление книги по ее уникальному идентификатору (ID).

- **Поиск книг**:
    - Поиск книг по названию, автору, году издания.

## Установка и настройка

### Требования

- Python 3.12 +

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Gricana/cli_library_manager.git
   cd cli_library_manager

### Использование

#### Запуск

Из корневой директории проекта (без параметров!):

  ```bash
  python main.py
  ```

Вы окажетесь в интерактивной консольной оболочке, где сможете выполнять
все доступные команды для управления хранилищем.

#### Доступные команды

1. Добавление книги
    ```bash
    add-book "<Название>" "<Автор>" <Год> [<Статус>]
    ```
   _Пример:_
    ```bash
    add-book "The Great Gatsby" "F. Scott Fitzgerald" 1925
    ```
   По умолчанию статус книги: в наличии.


2. Просмотр всех книг
    ```bash
    show-all 
    ```

   _Пример вывода:_
    ```bash
    ID                                   | TITLE                  | AUTHOR              | YEAR | STATUS   
    ------------------------------------------------------------------------------------------------------
    3bb236a3-5de3-467a-8502-7b4510d30c51 | Moby-Dick              | Herman Melville     | 1851 | в наличии
    057e226d-ef44-4b7f-901e-c2243cbcc05b | To Kill a Mockingbird  | Harper Lee          | 1960 | выдана
    ```
3. Обновление статуса книги
    ```bash
    update-status <ID> <Статус> 
    ```

   _Пример:_
    ```bash
    update-status 3bb236a3-5de3-467a-8502-7b4510d30c51 "выдана"
    ```

4. Удаление книги
    ```bash
    remove-book <ID>
    ```

   _Пример:_
    ```bash
    remove-book 3bb236a3-5de3-467a-8502-7b4510d30c51 
    ```

5. Поиск книг
    ```bash
    find-books <keyword> 
    ```

   _Пример:_
    ```bash
    find-books "Gatsby" 
    ```

#### Обработка ошибок

Команда с некорректным вводом вызовет соответствующее сообщение об ошибке.

_Пример:_

  ```bash
  add-book The Great Gatsby F. Scott Fitzgerald 1925
  ```

_Вывод:_

  ```bash
  usage: add-book [-h] title author year [{в наличии,выдана}]
  error: unrecognized arguments: The Great Gatsby F. Scott Fitzgerald 1925
  ```

### Тестирование

Для запуска тестов из корневой директории используйте команду:

С помощью unittest:

```bash
python -m unittest discover -s tests
```

## Архитектура проекта

Проект организован по модульной архитектуре с четким разделением
ответственности
между компонентами. Это обеспечивает удобство поддержки, расширения и
тестирования.

```markdown
.
├── cli
│ ├── commands.py
│ ├── decorators.py
│ ├── __init__.py
│ └── parser.py
├── data
│ └── books.json
├── main.py
├── manager
│ ├── __init__.py
│ └── manage.py
├── models
│ ├── book.py
│ ├── constants.py
│ ├── exceptions.py
│ ├── utils.py
│ └── validators
│ ├── base.py
│ ├── book.py
│ └── __init__.py
├── README.md
├── storage
│ ├── exceptions.py
│ ├── __init__.py
│ ├── interface.py
│ ├── json_storage.py
│ └── observer.py
└── tests
├── data
├── __init__.py
├── test_cli.py
├── test_manager.py
├── test_storage.py
└── test_validators.py
```

### Основные модули

1. **cli**

Модуль отвечает за взаимодействие с пользователем через командную строку.

* _commands.py:_ Реализует команды CLI, такие как добавление, удаление,
  обновление и поиск книг.
* _decorators.py:_ Содержит декораторы для логировая введённых команд.
* _parser.py:_ Реализует парсер для аргументов командной строки.

3. **data**

Содержит JSON-файл books.json, который используется для хранения информации о
книгах. Этот файл обрабатывается хранилищем данных (_storage_).

3. **main.py**

Главный файл запуска приложения. Инициализирует компоненты проекта и запускает
CLI-интерфейс.

4. **manager**

Содержит логику управления книгами.

* _manage.py:_ Основной файл управления, предоставляющий методы для добавления,
  удаления, обновления и поиска книг.

5. **models**

Модуль, содержащий модель данных и связанные утилиты.

* _book.py:_ Определяет структуру книги.
* _constants.py:_ Содержит константы и перечисления, такие как статусы книги.
* _exceptions.py:_ Определяет пользовательские исключения для обработки ошибок.
* _utils.py:_ Содержит вспомогательные функции.
* _**validators**_: Субмодуль для проверки данных.
    * _base.py:_ Базовые классы и утилиты для валидации.
    * _book.py:_ Проверка полей книги.

6. **storage**

Модуль для работы с хранилищем данных.

* _exceptions.py:_ Исключения, связанные с ошибками хранения данных.
* _interface.py:_ Интерфейс для реализации различных хранилищ.
* _json_storage.py:_ Реализация хранилища данных в формате JSON.
* _observer.py:_ Реализует паттерн "наблюдатель" для синхронизации изменений
  данных.

7. **tests**

Содержит тесты для проверки функциональности приложения.

* _test_cli.py:_ Тесты для проверки CLI-интерфейса.
* _test_manager.py:_ Тесты для проверки логики управления книгами.
* _test_storage.py:_ Тесты для проверки работы хранилища данных.
* _test_validators.py:_ Тесты для проверки валидаторов.

### Взаимодействие модулей

* CLI: Отвечает за взаимодействие с пользователем.
  Принимает команды, парсит их и вызывает соответствующие методы в manager.
* _Manager:_ Осуществляет управление данными, выполняя операции над объектами
  Book и взаимодействуя с модулем storage.
* _Storage:_ Обеспечивает сохранение и загрузку данных (например, из файла
  JSON).
* _Models:_ Содержит модель книги и обеспечивает проверку данных через
  валидаторы.
* _Tests:_ Обеспечивает тестирование каждого модуля, чтобы гарантировать
  стабильность приложения.

### Потенциальные расширения

1. [ ] Добавление нового типа хранилища (например, базы данных).
2. [ ] Поддержка веб-интерфейса вместо CLI.
3. [ ] Углубленная система фильтрации и сортировки книг.
4. [ ] Логирование действий пользователя в отдельный файл.

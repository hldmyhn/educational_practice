# hh.ru parser bot

Это телеграм бот для парсинга ваканский с сайта hh.ru и последующего поиска ваканский в нем по фильтрам.

## Установка

### Локальная установка

1. Склонируйте репозиторий:
     ```bash
     git clone https://github.com/hldmyhn/educational_practice.git
     cd educational_practice
     ```

2. Установите зависимости:
     ```bash
     pip install -r requirements.txt
     ```

3. Запустите приложение:
     ```bash
     python ./src/__main__.py
     ```

### Docker 🐳

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/hldmyhn/educational_practice.git
    cd educational_practice
    ```

2. Запустите Docker контейнер:

    ```bash
    docker-compose up -d --build
    ```

## Стэк технологий

aiogram - современный ассинхронный фреймворк для создания telegram ботов.

aiogram_dialog - это GUI для telegram ботов. Он вдохновлен идеями Android SDK и React.js.

MySQL - база данных

## Структура БД

### Таблица vacancies

| Поле        | Тип данных | Описание                          |
|-------------|------------|-----------------------------------|
| id          | INT        | Уникальный идентификатор вакансии |
| name        | VARCHAR    | Название вакансии                 |
| employment  | VARCHAR    | Тип занятости                     |
| requirement | VARCHAR    | Требования к кандидатам           |
| experience  | VARCHAR    | Требуемый опыт работы             |

### Описание полей:

- `id`: Уникальный идентификатор вакансии, является первичным ключом.
- `name`: Название вакансии, текстовое поле, не может быть пустым.
- `employment`: Тип занятости для вакансии (полная занятость, частичная занятость и т.д.), также текстовое поле.
- `requirement`: Требования к кандидатам для вакансии, текстовое поле.
- `experience`: Требуемый опыт работы для вакансии, текстовое поле.

![Пример работы бота](/video/1.gif)



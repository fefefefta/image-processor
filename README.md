# image-processor
Проект представляет из себя три сервиса, отвечающих за обработку изображений, сохранение обработанных изображений в БД и файловую систему и предоставление API для добавления изображений и просмотра списка добавленных изображений.

## Запуск
Для запуска проекта:
```bash
docker compose up --build
```

# Image Processor API

Этот сервис предоставляет REST API для загрузки изображений и их описаний, хранения метаданных в базе данных PostgreSQL, а также отправки данных в очередь сообщений Redis.

## Как это работает?

### 1. **Загрузка изображения**:
   - Пользователь загружает изображение в формате JPEG вместе с текстовым описанием (до 200 символов).
   - Сервис сохраняет изображение в файловую систему, а метаданные (включая описание и путь к изображению) — в базу данных PostgreSQL.

### 2. **Очередь сообщений**:
   - После успешной загрузки изображение и его метаданные помещаются в очередь Redis.
   - Эти данные будут использованы другими сервисами для дальнейшей обработки и сохранения.

### 3. **API Вызовы**:
С вызовами также можно ознакомиться по ручке /docs (документация Swagger)

#### POST `/api/images`
   - Загрузка изображения с описанием.
   - Ожидаемые параметры:
     - `file`: изображение в формате JPEG.
     - `description`: текстовое описание изображения.
   - Ответ:
     - `201 Created`: содержит ID изображения и ссылку для его получения.

#### GET `/api/images`
   - Получение списка всех загруженных изображений.
   - Ответ:
     - `200 OK`: список всех изображений с их ID, описанием, временем загрузки и ссылками на изображения.

#### GET `/api/images/{id}`
   - Получение информации об изображении по его ID.
   - Ответ:
     - `200 OK`: информация об изображении, включая описание, время загрузки и ссылку на изображение.
     - `404 Not Found`: если изображение с данным ID не найдено.

### 4. **Работа с базой данных**:
   - Для хранения информации об изображениях используется PostgreSQL. Таблица `image_records` хранит:
     - `id`: уникальный идентификатор записи.
     - `timestamp`: время загрузки изображения.
     - `description`: текстовое описание изображения.
     - `image_path`: путь к сохраненному изображению на файловой системе.

# Image Processing Service

Этот сервис занимается обработкой изображений из очереди Redis. Он добавляет текстовое описание в нижнюю часть изображения.

## Как это работает?

1. **Получение изображения**:
   - Сервис постоянно ждёт, когда появится новая задачка в очереди Redis.
   - Как только задача появляется, сервис начинает обработку.

2. **Обработка текста**:
   - Текст аккуратно делится на строки, чтобы не лезть за пределы картинки.
   - Если текст вдруг оказался длиннее, чем ожидалось, он будет переноситься на новую строку.
   - Шрифт — `Arial`.

3. **Остальное**:
   - Далее результат отправляется обратно в другую очередь Redis, им займется сервис сохранения данных.

# Image Saver Service

Этот сервис отвечает за сохранение обработанных изображений и связанных с ними данных. Изображения и их метаданные извлекаются из очереди Redis, после чего изображение сохраняется в файловой системе, а информация о нем — в базе данных PostgreSQL.

## Как это работает?

1. **Извлечение сообщения из Redis**:
   - Сервис постоянно мониторит очередь Redis, ожидая появления новых сообщений.
   - Как только сообщение поступает, оно извлекается и десериализуется.

2. **Сохранение изображения**:
   - Извлеченные из сообщения байты изображения сохраняются в директорию `media/`.
   - Имя файла формируется на основе уникального идентификатора изображения.

3. **Сохранение данных в базе данных**:
   - Сервис сохраняет в базу данных PostgreSQL метаданные изображения:
     - Временную метку (`timestamp`), преобразованную из формата ISO 8601.
     - Описание изображения.
     - Путь к сохраненному файлу изображения.

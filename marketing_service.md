## МИНИСТЕРСТВО ОБРАЗОВАНИЯ, НАУКИ И МОЛОДЕЖНОЙ ПОЛИТИКИ РЕСПУБЛИКИ КОМИ

Государственное профессиональное образовательное учереждение "Сыктывкарский политехнический техникум"

## Курсовая работа

Тема: база данных издательства подсистема служба маркетинга

**Профессия / специальность** 

Информационные системы и программирование

**Выполнила**

Овчинникова Арина Игоревна 

Дневная, 4 курс, 414 гр.

**Руководитель**

Пунгин И.В.


### Введение 


 # Задание на курсовую работу по МДК 11.01 "Технология разработки и защиты баз данных"

[comment]: # (Комментарий: задание на курсовую работу заполняется студентом самостоятельно на основе темы его работы, изучаемых вопросов, срока представления работы к защите)

Специальность: <ins> 09.02.07 "Информационные системы и программирование"  </ins>

Тема курсовой работы: база данных Издательства. Подсистема служба маркетинга

Срок представления работы к защите: <ins> 15 ноября 2024 года. </ins>

Перечень подлежащих разработке вопросов:

[comment]: # (Комментарий: перечень вопросов перерабатывается студентом исходя из его темы)
## 1. Анализ предметной области. Постановка задачи.
## 1.1. Описание предметной области и функции решаемых задач.

Предметная область базы данных издательства с подсистемой службы маркетинга охватывает все аспекты, связанные с публикацией книг, управлением авторами, взаимодействием с клиентами и проведением маркетинговых акций. В данном контексте издательство — это организация, занимающаяся созданием, распространением и продажей книг, а служба маркетинга отвечает за продвижение продукции, привлечение клиентов и анализ результатов маркетинговых мероприятий.
Основные элементы предметной области:

    Авторы: Лица, создающие литературные произведения. Информация о них включает биографию, дату рождения.

    Книги: Издательская продукция, содержащая литературные произведения. Включает название, жанр, дату публикации, цену и количество доступных экземпляров.

    Клиенты: Лица, покупающие книги. Информация о клиентах включает имя, фамилию, контактные данные и дату регистрации.

    Маркетинговые акции: Специальные мероприятия, направленные на продвижение книг, которые могут включать скидки, специальные предложения и рекламные кампании.

    Продажи: Записи о транзакциях, связанных с покупкой книг клиентами. Включает информацию о количестве проданных экземпляров и общей сумме продажи.

    Результаты акций: Анализ эффективности проведенных маркетинговых мероприятий, включая общую сумму продаж и отзывы клиентов.

Функции решаемых задач

База данных подсистемы службы маркетинга в издательстве решает множество задач, включая, но не ограничиваясь следующими:

    Управление авторами:
        Хранение и обновление информации об авторах.
        Поддержка связи между авторами и их произведениями.

    Управление книгами:
        Ведение каталога книг с возможностью добавления, редактирования и удаления записей.
        Отслеживание наличия книг на складе.

    Управление клиентами:
        Регистрация новых клиентов и хранение их контактной информации.
        Ведение истории покупок клиентов для анализа их предпочтений.

    Планирование и проведение маркетинговых акций:
        Создание и управление маркетинговыми кампаниями, включая установление сроков, описания и скидок.
        Автоматизация рассылок и уведомлений о текущих акциях для клиентов.

    Анализ продаж:
        Отслеживание и анализ данных о продажах для оценки эффективности книг и акций.
        Генерация отчетов о продажах по различным критериям (по времени, по клиентам, по книгам и т.д.).

    Оценка результатов акций:
        Сбор и анализ данных о результатах проведенных маркетинговых мероприятий.
        Оценка влияния акций на продажи и получение отзывов от клиентов для улучшения будущих кампаний.

    Поддержка принятия решений:
        Предоставление аналитических данных для стратегического планирования и разработки новых маркетинговых стратегий.
        Помощь в определении целевой аудитории и предпочтений клиентов.

## 1.2. Перечень входных данных.

1. Данные об авторах
    Имя автора: Полное имя автора.
    Биография: Краткая информация о жизни и творчестве автора.
    Дата рождения: Дата рождения автора.
   
2. Данные о книгах
    Название книги: Полное название книги.
    Автор: Идентификатор автора (внешний ключ, ссылающийся на таблицу авторов).
    Жанр: Жанр книги (например, роман, научная фантастика, учебник и т.д.).
    Дата публикации: Дата, когда книга была опубликована.
    Цена: Розничная цена книги.
    Количество на складе: Количество доступных экземпляров книги.

3. Данные о клиентах
    Имя клиента: Имя клиента.
    Фамилия клиента: Фамилия клиента.
    Электронная почта: Адрес электронной почты клиента (должен быть уникальным).
    Телефон: Номер телефона клиента.
    Дата регистрации: Дата, когда клиент зарегистрировался в системе.

4. Данные о маркетинговых акциях
    Название кампании: Название маркетинговой акции.
    Дата начала: Дата начала акции.
    Дата окончания: Дата завершения акции.
    Описание: Подробное описание акции.
    Процент скидки: Скидка, предлагаемая в рамках акции.

5. Данные о продажах
    Книга: Идентификатор книги (внешний ключ, ссылающийся на таблицу книг).
    Клиент: Идентификатор клиента (внешний ключ, ссылающийся на таблицу клиентов).
    Дата продажи: Дата, когда была совершена продажа.
    Количество: Количество проданных экземпляров.
    Общая сумма: Общая сумма продажи (рассчитывается на основе цены и количества).

6. Данные о результатах акций
    Кампания: Идентификатор маркетинговой кампании (внешний ключ, ссылающийся на таблицу маркетинговых акций).
    Общая сумма продаж: Общая сумма, полученная от продаж в рамках акции.
    Количество продаж: Общее количество продаж, совершенных в рамках акции.
    Отзыв: Отзывы клиентов о проведенной акции (если применимо).

## 1.3. Перечень выходных данных

1. Выходные данные о авторах
    Список авторов: Полное имя, дата рождения, краткая биография.
    Количество книг у каждого автора: Общее количество книг, написанных каждым автором.
    Детальная информация об авторе: Полное имя, биография, дата рождения, список книг, написанных автором.

2. Выходные данные о книгах
    Список книг: Название книги, автор, жанр, дата публикации, цена, количество на складе.
    Книги по жанрам: Список книг, сгруппированный по жанрам.
    Книги с низким запасом: Список книг, количество которых на складе ниже заданного порога.
    Информация о наличии: Книги, доступные на складе и их количество.

3. Выходные данные о клиентах
    Список клиентов: Имя, фамилия, электронная почта, телефон, дата регистрации.
    Клиенты по количеству покупок: Список клиентов, отсортированный по количеству совершенных покупок.
    Клиенты, зарегистрированные за определенный период: Список клиентов, которые зарегистрировались в системе за указанный период времени.

4. Выходные данные о маркетинговых акциях
    Список активных акций: Название кампании, дата начала, дата окончания, процент скидки.
    Эффективность акций: Сравнение общей суммы продаж до и после проведения акций.
    Результаты акций: Общая сумма продаж и количество продаж для каждой акции.

5. Выходные данные о продажах
    Отчет о продажах: Дата продажи, название книги, имя клиента, количество проданных экземпляров, общая сумма.
    Продажи по времени: Статистика продаж по дням, месяцам или годам.
    Продажи по книгам: Список книг с количеством проданных экземпляров и общей суммой продаж.
    Продажи по клиентам: Список клиентов с количеством и общей суммой их покупок.

6. Выходные данные о результатах акций
    Общая эффективность акций: Общая сумма продаж и количество продаж для каждой маркетинговой акции.
    Отзывы клиентов: Сводка отзывов клиентов о проведенных акциях.
    Сравнительный анализ акций: Сравнение результатов разных акций для выявления наиболее эффективных.

7. Общие выходные данные для анализа
    Анализ доходов: Общая сумма доходов за определенный период, разбитая по категориям (книги, акции и т.д.).
    Анализ клиентской базы: Сегментация клиентов по различным критериям (например, по количеству покупок, сумме покупок и т.д.).
    Тенденции продаж: Графическое представление продаж по времени для выявления сезонных тенденций.
    Эффективность маркетинговых акций: Сравнение результатов акций по общему доходу и количеству продаж.

## 1.4. Ограничения предметной области (если таковые имеются).

    Конфиденциальность данных:
        Защита личной информации клиентов.
        Ограничение доступа к данным только для авторизованных пользователей.

    Целостность данных:
        Обеспечение ссылочной целостности между таблицами (например, между клиентами и их заказами).
        Проверка корректности вводимых данных (например, формат электронной почты).

    Согласованность данных:
        Обновление данных должно происходить в соответствии с установленными правилами (например, изменение статуса заказа).

    Соблюдение законодательства:
        Соответствие требованиям законодательства о защите персональных данных .

## 1.5. Взаимодействие с другими программами.
1. API (Application Programming Interface)
    RESTful API: Создание RESTful API позволяет другим приложениям взаимодействовать с базой данных через HTTP-запросы. Это может быть полезно для интеграции с веб-приложениями, мобильными приложениями и сторонними сервисами.
    SOAP API: В некоторых случаях может использоваться SOAP для более сложных интеграций, особенно в корпоративных системах.

2. Импорт и Экспорт Данных
    CSV и Excel: Поддержка импорта и экспорта данных в форматах CSV или Excel позволяет пользователям легко загружать данные о клиентах, продажах и акциях из других систем или экспортировать их для анализа.
    XML и JSON: Эти форматы могут использоваться для обмена данными с другими системами, особенно если они требуют структурированных данных.

3. Интеграция с CRM-системами
    База данных может быть интегрирована с CRM-системами (например, Salesforce, HubSpot) для управления клиентами и отслеживания взаимодействий. Это позволяет автоматизировать процессы маркетинга и продаж, а также улучшить анализ данных о клиентах.

4. Взаимодействие с системами аналитики
    BI-инструменты: Интеграция с инструментами бизнес-аналитики (например, Tableau, Power BI) позволяет извлекать данные из базы данных для создания отчетов и визуализаций.
    Анализ данных: Использование SQL-запросов для извлечения данных и анализа их в сторонних аналитических системах.

5. Интеграция с системами управления контентом (CMS)
    База данных может взаимодействовать с CMS (например, WordPress, Drupal) для автоматического обновления информации о книгах, авторах и акциях на веб-сайте издательства.

6. Автоматизация процессов
    Скрипты и задачи: Использование скриптов (например, на Python, PHP) для автоматизации процессов, таких как резервное копирование данных, обновление информации и синхронизация с другими системами.
    Планировщики задач: Интеграция с планировщиками задач (например, Cron на Linux) для автоматического выполнения заданий по расписанию.

7. Взаимодействие с платежными системами
    Интеграция с платежными системами (например, PayPal, Stripe) для обработки онлайн-продаж. Это позволяет автоматически обновлять информацию о продажах в базе данных.

8. Обмен данными с другими базами данных
    ETL-процессы: Использование процессов извлечения, трансформации и загрузки (ETL) для интеграции данных из различных источников и систем в одну базу данных.
    Синхронизация: Настройка синхронизации данных между различными базами данных для обеспечения актуальности информации.

## 2. Инфологическая (концептуальная) модель базы данных.

## 2.1. Выделение информационных объектов.
   
   Авторы, книги, клиенты, маркетинговые акции,продажи, результаты акций
   
 ## 2.2. Определение атрибутов объектов.
 
Атрибуты объектов, как правило, представляют собой характеристики, которые могут быть использованы для хранения информации о каждом объекте. Ниже приведены атрибуты для каждого из выделенных объектов:

    Авторы
        ID: уникальный идентификатор (целое число)
        Имя: строка
        Фамилия: строка
        Дата рождения: дата
        Национальность: строка
        Биография: текст

    Книги
        ID: уникальный идентификатор (целое число)
        Заголовок: строка
        Жанр: строка
        Дата публикации: дата
        ISBN: строка
        Количество страниц: целое число
        Цена: десятичное число
        ID автора: целое число (внешний ключ)

    Клиенты
        ID: уникальный идентификатор (целое число)
        Имя: строка
        Фамилия: строка
        Email: строка (уникальный)
        Телефон: строка
        Адрес: строка
        Дата регистрации: дата

    Маркетинговые акции
        ID: уникальный идентификатор (целое число)
        Название акции: строка
        Описание: текст
        Дата начала: дата
        Дата окончания: дата
        Скидка: десятичное число
        Условия участия: текст

    Продажи
        ID: уникальный идентификатор (целое число)
        ID клиента: целое число (внешний ключ)
        ID книги: целое число (внешний ключ)
        Дата продажи: дата
        Количество: целое число
        Общая сумма: десятичное число

    Результаты акций
        ID: уникальный идентификатор (целое число)
        ID акции: целое число (внешний ключ)
        ID книги: целое число (внешний ключ)
        Количество проданных единиц: целое число
        Общая выручка: десятичное число
        Отзывы клиентов: текст
## 2.3. Определение отношений и мощности отношений между объектами.
Отношения между объектами

    Авторы и Книги
        Отношение: Один ко многим (1:N)
        Описание: Один автор может написать несколько книг, но каждая книга имеет только одного автора.
        Мощность:
            Один автор → много книг
            Например, если у нас есть 10 авторов, и каждый из них написал 5 книг, то мощность отношения будет 10:50.

    Клиенты и Продажи
        Отношение: Один ко многим (1:N)
        Описание: Один клиент может совершить несколько покупок (продаж), но каждая продажа относится только к одному клиенту.
        Мощность:
            Один клиент → много продаж
            Например, если у нас есть 100 клиентов, и каждый из них совершил по 3 продажи, то мощность отношения будет 100:300.

    Книги и Продажи
        Отношение: Один ко многим (1:N)
        Описание: Одна книга может быть продана многими клиентами, но каждая продажа относится только к одной книге.
        Мощность:
            Одна книга → много продаж
            Например, если у нас есть 50 книг, и каждая из них была продана 10 раз, то мощность отношения будет 50:500.

    Маркетинговые акции и Книги
        Отношение: Многие ко многим (M:N)
        Описание: Одна маркетинговая акция может быть связана с несколькими книгами, и одна книга может участвовать в нескольких акциях.
        Мощность:
            Много акций → много книг
            Например, если у нас есть 5 акций, и каждая из них охватывает 4 книги, а каждая книга участвует в 2 акциях, то мощность отношения будет 5:20 (если считать уникальные пары) или 20:20 (если учитывать все связи).

    Маркетинговые акции и Результаты акций
        Отношение: Один ко многим (1:N)
        Описание: Каждая маркетинговая акция может иметь несколько результатов, но каждый результат относится только к одной акции.
        Мощность:
            Одна акция → много результатов
            Например, если у нас есть 10 акций, и каждая акция имеет 3 результата, то мощность отношения будет 10:30.

    Книги и Результаты акций
        Отношение: Один ко многим (1:N)
        Описание: Одна книга может иметь несколько результатов акций, но каждый результат относится только к одной книге.
        Мощность:
            Одна книга → много результатов
            Например, если у нас есть 50 книг, и каждая книга имеет 2 результата акций, то мощность отношения будет 50:100.

## 2.4. Построение концептуальной модели.

## 3. Логическая структура БД.

## 4. Физическая структура базы данных.

## 5. Реализация проекта в среде конкретной СУБД.
## 5.1. Создание таблиц.
## 5.2. Создание запросов.
## 5.3. Разработка интерфейса.
## 5.4. Назначение прав доступа.
## 5.5. Создание индексов.
## 5.6. Разработка стратегии резервного копирования базы данных


Руководитель работы __________________ <ins> И. В. Пунгин </ins>

Задание принял к исполнению _______________________________ <ins> Инициалы и Фамилия студента

[comment]: # (Комментарий: Инициалы и Фамилия студента должны быть заменены студентом на свои инициалы и фамилию.)

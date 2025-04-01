--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: user_role; Type: TYPE; Schema: public; Owner: marketing_service
--

CREATE TYPE public.user_role AS ENUM (
    'Администратор',
    'Маркетолог',
    'Клиент'
);


ALTER TYPE public.user_role OWNER TO marketing_service;

--
-- Name: update_sequence_after_delete(); Type: FUNCTION; Schema: public; Owner: marketing_service
--

CREATE FUNCTION public.update_sequence_after_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_val BIGINT;
BEGIN
    EXECUTE format('SELECT setval(''%s_%s_seq'', (SELECT COALESCE(MAX(%s), 0) + 1 FROM %s))',
                   TG_TABLE_NAME, TG_ARGV[0], TG_ARGV[0], TG_TABLE_NAME);
    
    -- Получаем текущее значение последовательности
    EXECUTE format('SELECT last_value FROM %s_%s_seq', TG_TABLE_NAME, TG_ARGV[0]) INTO new_val;
    
    -- Выводим сообщение
    RAISE NOTICE 'Последовательность обновлена: %', new_val;
    
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.update_sequence_after_delete() OWNER TO marketing_service;

--
-- Name: administrators_administrator_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.administrators_administrator_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.administrators_administrator_id_seq OWNER TO marketing_service;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administrators; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.administrators (
    administrator_id integer DEFAULT nextval('public.administrators_administrator_id_seq'::regclass) NOT NULL,
    user_id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    phone character varying(20) NOT NULL
);


ALTER TABLE public.administrators OWNER TO marketing_service;

--
-- Name: authors_author_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.authors_author_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.authors_author_id_seq OWNER TO marketing_service;

--
-- Name: authors; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.authors (
    author_id integer DEFAULT nextval('public.authors_author_id_seq'::regclass) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    bio text
);


ALTER TABLE public.authors OWNER TO marketing_service;

--
-- Name: book_authors; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.book_authors (
    book_id integer NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.book_authors OWNER TO marketing_service;

--
-- Name: books_book_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.books_book_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_book_id_seq OWNER TO marketing_service;

--
-- Name: books; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.books (
    book_id integer DEFAULT nextval('public.books_book_id_seq'::regclass) NOT NULL,
    title character varying(255) NOT NULL,
    genre character varying(100),
    published_date date DEFAULT CURRENT_DATE,
    price numeric(10,2) NOT NULL,
    stock integer NOT NULL,
    CONSTRAINT books_stock_check CHECK ((stock >= 0))
);


ALTER TABLE public.books OWNER TO marketing_service;

--
-- Name: campaigns_campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.campaigns_campaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.campaigns_campaign_id_seq OWNER TO marketing_service;

--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.campaigns (
    campaign_id integer DEFAULT nextval('public.campaigns_campaign_id_seq'::regclass) NOT NULL,
    campaign_name character varying(255) NOT NULL,
    start_date date DEFAULT CURRENT_DATE NOT NULL,
    end_date date DEFAULT (CURRENT_DATE + '30 days'::interval) NOT NULL,
    budget numeric(12,2) NOT NULL,
    description text,
    marketer_id integer,
    CONSTRAINT campaigns_budget_check CHECK ((budget >= (0)::numeric)),
    CONSTRAINT valid_dates CHECK ((end_date >= start_date))
);


ALTER TABLE public.campaigns OWNER TO marketing_service;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.customers_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO marketing_service;

--
-- Name: customers; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.customers (
    customer_id integer DEFAULT nextval('public.customers_customer_id_seq'::regclass) NOT NULL,
    user_id integer,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    phone character varying(20),
    address text
);


ALTER TABLE public.customers OWNER TO marketing_service;

--
-- Name: marketers_marketer_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.marketers_marketer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marketers_marketer_id_seq OWNER TO marketing_service;

--
-- Name: marketers; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.marketers (
    marketer_id integer DEFAULT nextval('public.marketers_marketer_id_seq'::regclass) NOT NULL,
    user_id integer NOT NULL,
    department character varying(255) NOT NULL,
    phone character varying(20) NOT NULL,
    current_projects text,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL
);


ALTER TABLE public.marketers OWNER TO marketing_service;

--
-- Name: marketing_materials_material_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.marketing_materials_material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.marketing_materials_material_id_seq OWNER TO marketing_service;

--
-- Name: marketing_materials; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.marketing_materials (
    material_id integer DEFAULT nextval('public.marketing_materials_material_id_seq'::regclass) NOT NULL,
    campaign_id integer,
    material_type character varying(100) NOT NULL,
    content text NOT NULL,
    distribution_date date DEFAULT CURRENT_DATE
);


ALTER TABLE public.marketing_materials OWNER TO marketing_service;

--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_order_id_seq OWNER TO marketing_service;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.orders (
    order_id integer DEFAULT nextval('public.orders_order_id_seq'::regclass) NOT NULL,
    customer_id integer,
    order_date date DEFAULT CURRENT_DATE NOT NULL,
    total_amount numeric(10,2) NOT NULL,
    title character varying(255),
    genre character varying(255),
    CONSTRAINT orders_total_amount_check CHECK ((total_amount >= (0)::numeric))
);


ALTER TABLE public.orders OWNER TO marketing_service;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: marketing_service
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO marketing_service;

--
-- Name: users; Type: TABLE; Schema: public; Owner: marketing_service
--

CREATE TABLE public.users (
    user_id integer DEFAULT nextval('public.users_user_id_seq'::regclass) NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role public.user_role NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO marketing_service;

--
-- Data for Name: administrators; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.administrators (administrator_id, user_id, first_name, last_name, phone) FROM stdin;
1	1	Иван	Петров	+79001234567
2	6	Ольга	Сидорова	+79161234567
3	11	Алексей	Смирнов	+79261234567
4	12	Екатерина	Иванова	+79361234567
5	13	Дмитрий	Кузнецов	+79461234567
6	14	Мария	Попова	+79561234567
7	15	Сергей	Васильев	+79661234567
8	16	Анна	Семенова	+79761234567
9	17	Андрей	Павлов	+79861234567
10	18	Татьяна	Федорова	+79961234567
\.


--
-- Data for Name: authors; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.authors (author_id, first_name, last_name, bio) FROM stdin;
1	Лев	Толстой	Классик русской литературы
2	Федор	Достоевский	Автор психологических романов
3	Антон	Чехов	Мастер короткого рассказа
4	Александр	Пушкин	Основоположник современного русского языка
5	Николай	Гоголь	Создатель мистических произведений
6	Иван	Тургенев	Представитель реализма
7	Михаил	Булгаков	Автор "Мастера и Маргариты"
8	Александр	Солженицын	Лауреат Нобелевской премии
9	Владимир	Набоков	Русский и американский писатель
10	Борис	Пастернак	Поэт и прозаик
11	Илья	Ильф	Русский советский писатель
12	Евгений	Петров	Русский советский писатель
\.


--
-- Data for Name: book_authors; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.book_authors (book_id, author_id) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	1
12	11
12	12
\.


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.books (book_id, title, genre, published_date, price, stock) FROM stdin;
1	Война и мир	Роман	1869-01-01	1500.00	100
2	Преступление и наказание	Роман	1866-01-01	1200.00	80
3	Вишневый сад	Пьеса	1904-01-01	800.00	50
4	Евгений Онегин	Роман в стихах	1833-01-01	900.00	70
5	Мертвые души	Поэма	1842-01-01	950.00	60
6	Отцы и дети	Роман	1862-01-01	850.00	90
7	Мастер и Маргарита	Роман	1967-01-01	1300.00	120
8	Архипелаг ГУЛАГ	Художественно-историческое	1973-01-01	2000.00	40
9	Лолита	Роман	1955-01-01	1100.00	75
10	Доктор Живаго	Роман	1957-01-01	1400.00	65
11	Детство	Повесть	2025-03-20	1700.00	76
12	Двенадцать стульев	Роман	2025-03-30	250.00	54
\.


--
-- Data for Name: campaigns; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.campaigns (campaign_id, campaign_name, start_date, end_date, budget, description, marketer_id) FROM stdin;
1	Летняя распродажа	2024-06-01	2024-08-31	500000.00	Скидки на классику	1
2	Новинки осени	2024-09-01	2024-11-30	750000.00	Продвижение новых книг	1
3	Рождественские скидки	2024-12-01	2024-12-31	300000.00	Праздничные предложения	1
4	Весеннее обновление	2025-03-01	2025-05-31	400000.00	Акции к 8 марта	2
5	Школьная программа	2024-09-01	2025-05-31	600000.00	Книги для учебы	2
6	Книжная ярмарка	2024-10-01	2024-10-07	200000.00	Ежегодное мероприятие	2
7	Электронные книги	2024-07-01	2024-09-30	350000.00	Распродажа eBooks	3
8	Подарочные издания	2024-12-15	2025-01-15	450000.00	Подарки к Новому году	3
9	Авторские встречи	2024-04-01	2024-06-30	250000.00	Мероприятия с писателями	3
10	Детская литература	2024-05-01	2024-07-31	300000.00	Книги для детей	3
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.customers (customer_id, user_id, first_name, last_name, email, phone, address) FROM stdin;
1	3	Алексей	Комаров	client1@mail.com	+79123456789	ул. Ленина, 1
2	4	Марина	Соколова	client2@mail.com	+79223456789	ул. Пушкина, 2
3	7	Владимир	Лебедев	client3@mail.com	+79323456789	пр. Мира, 3
4	8	Евгения	Новикова	client4@mail.com	+79423456789	ул. Садовая, 4
5	10	Андрей	Морозов	client5@mail.com	+79523456789	ул. Центральная, 5
6	26	Татьяна	Воробьева	client6@mail.com	+79623456789	пр. Победы, 6
7	27	Сергей	Егоров	client7@mail.com	+79723456789	ул. Зеленая, 7
8	28	Ольга	Ковалева	client8@mail.com	+79823456789	ул. Лесная, 8
9	29	Денис	Соловьев	client9@mail.com	+79923456789	пр. Космонавтов, 9
10	30	Ирина	Ильина	client10@mail.com	+79033456789	ул. Речная, 10
\.


--
-- Data for Name: marketers; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.marketers (marketer_id, user_id, department, phone, current_projects, first_name, last_name) FROM stdin;
1	2	Digital	+79111234567	Проект А	Анна	Иванова
2	5	SMM	+79211234567	Проект Б	Дмитрий	Смирнов
3	9	SEO	+79311234567	Проект В	Елена	Петрова
4	19	Контент	+79411234567	Проект Г	Михаил	Козлов
5	20	Аналитика	+79511234567	Проект Д	Ольга	Никитина
6	21	PR	+79611234567	Проект Е	Павел	Морозов
7	22	Email	+79711234567	Проект Ж	Юлия	Волкова
8	23	PPC	+79811234567	Проект З	Игорь	Алексеев
9	24	Видео	+79911234567	Проект И	Наталья	Орлова
10	25	Мобильные	+79021234567	Проект К	Артем	Белов
\.


--
-- Data for Name: marketing_materials; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.marketing_materials (material_id, campaign_id, material_type, content, distribution_date) FROM stdin;
1	1	Email	Приветственное письмо	2024-05-25
2	2	Баннер	Реклама 1200x600	2024-08-20
3	3	Видео	Ролик 30 сек	2024-11-15
4	4	Соцсети	Посты для Instagram	2025-02-20
5	5	Брошюра	PDF каталог	2024-08-01
6	6	Радио	Аудиореклама	2024-09-20
7	7	Landing Page	Целевая страница	2024-06-15
8	8	Печать	Буклеты А4	2024-12-01
9	9	Вебинар	Онлайн-трансляция	2024-03-25
10	10	Мобильное приложение	Push-уведомления	2024-04-20
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.orders (order_id, customer_id, order_date, total_amount, title, genre) FROM stdin;
1	1	2024-03-01	1500.00	Война и мир	Роман
2	2	2024-03-02	2400.00	Преступление и наказание	Роман
3	3	2024-03-03	1750.00	Вишневый сад	Пьеса
4	4	2024-03-04	3200.00	Евгений Онегин	Роман в стихах
5	5	2024-03-05	2850.00	Мертвые души	Поэма
6	6	2024-03-06	4100.00	Отцы и дети	Роман
7	7	2024-03-07	1950.00	Мастер и Маргарита	Роман
8	8	2024-03-08	2250.00	Архипелаг ГУЛАГ	Художественно-историческое
9	9	2024-03-09	3600.00	Лолита	Роман
10	10	2024-03-10	2750.00	Доктор Живаго	Роман
12	1	2025-03-23	435.00	Детство	Повесть
14	1	2025-03-27	2154.00	test	Роман
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: marketing_service
--

COPY public.users (user_id, username, password_hash, role, created_at) FROM stdin;
4	client2	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Клиент	2024-01-04 12:00:00
5	marketer2	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Маркетолог	2024-01-05 13:00:00
6	admin2	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Администратор	2024-01-06 14:00:00
7	client3	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Клиент	2024-01-07 15:00:00
8	client4	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Клиент	2024-01-08 16:00:00
9	marketer3	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Маркетолог	2024-01-09 17:00:00
10	client5	d6d0c8e8a8b5d6c5e0e5e7a5d5c5e5e5	Клиент	2024-01-10 18:00:00
11	admin3	hash3	Администратор	2024-03-16 09:00:00
12	admin4	hash4	Администратор	2024-03-16 10:00:00
13	admin5	hash5	Администратор	2024-03-16 11:00:00
14	admin6	hash6	Администратор	2024-03-16 12:00:00
15	admin7	hash7	Администратор	2024-03-16 13:00:00
16	admin8	hash8	Администратор	2024-03-16 14:00:00
17	admin9	hash9	Администратор	2024-03-16 15:00:00
18	admin10	hash10	Администратор	2024-03-16 16:00:00
19	marketer4	hash11	Маркетолог	2024-03-16 17:00:00
20	marketer5	hash12	Маркетолог	2024-03-16 18:00:00
21	marketer6	hash13	Маркетолог	2024-03-16 19:00:00
22	marketer7	hash14	Маркетолог	2024-03-16 20:00:00
23	marketer8	hash15	Маркетолог	2024-03-16 21:00:00
24	marketer9	hash16	Маркетолог	2024-03-16 22:00:00
25	marketer10	hash17	Маркетолог	2024-03-16 23:00:00
26	client6	hash18	Клиент	2024-03-17 09:00:00
27	client7	hash19	Клиент	2024-03-17 10:00:00
28	client8	hash20	Клиент	2024-03-17 11:00:00
29	client9	hash21	Клиент	2024-03-17 12:00:00
30	client10	hash22	Клиент	2024-03-17 13:00:00
1	admin1	25f43b1486ad95a1398e3eeb3d83bc4010015fcc9bedb35b432e00298d5021f7	Администратор	2024-01-01 09:00:00
2	marketer1	7297155982ac6a9f5354c076405af4970272d483ba7b329c071b3a1e4aaa9a6b	Маркетолог	2024-01-02 10:00:00
3	client1	1917e33407c28366c8e3b975b17e7374589312676b90229adb4ce6e58552e223	Клиент	2024-01-03 11:00:00
\.


--
-- Name: administrators_administrator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.administrators_administrator_id_seq', 10, true);


--
-- Name: authors_author_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.authors_author_id_seq', 12, true);


--
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.books_book_id_seq', 13, true);


--
-- Name: campaigns_campaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.campaigns_campaign_id_seq', 13, true);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.customers_customer_id_seq', 11, true);


--
-- Name: marketers_marketer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.marketers_marketer_id_seq', 12, true);


--
-- Name: marketing_materials_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.marketing_materials_material_id_seq', 13, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 14, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: marketing_service
--

SELECT pg_catalog.setval('public.users_user_id_seq', 31, true);


--
-- Name: administrators administrators_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_pkey PRIMARY KEY (administrator_id);


--
-- Name: administrators administrators_user_id_key; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_user_id_key UNIQUE (user_id);


--
-- Name: authors authors_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (author_id);


--
-- Name: book_authors book_authors_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.book_authors
    ADD CONSTRAINT book_authors_pkey PRIMARY KEY (book_id, author_id);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (book_id);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (campaign_id);


--
-- Name: customers customers_email_key; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: marketers marketers_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.marketers
    ADD CONSTRAINT marketers_pkey PRIMARY KEY (marketer_id);


--
-- Name: marketers marketers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.marketers
    ADD CONSTRAINT marketers_user_id_key UNIQUE (user_id);


--
-- Name: marketing_materials marketing_materials_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.marketing_materials
    ADD CONSTRAINT marketing_materials_pkey PRIMARY KEY (material_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: books trg_books_after_delete; Type: TRIGGER; Schema: public; Owner: marketing_service
--

CREATE TRIGGER trg_books_after_delete AFTER DELETE ON public.books FOR EACH STATEMENT EXECUTE FUNCTION public.update_sequence_after_delete('book_id');


--
-- Name: users trg_users_after_delete; Type: TRIGGER; Schema: public; Owner: marketing_service
--

CREATE TRIGGER trg_users_after_delete AFTER DELETE ON public.users FOR EACH STATEMENT EXECUTE FUNCTION public.update_sequence_after_delete('user_id');


--
-- Name: administrators administrators_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: book_authors book_authors_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.book_authors
    ADD CONSTRAINT book_authors_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(author_id);


--
-- Name: book_authors book_authors_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.book_authors
    ADD CONSTRAINT book_authors_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(book_id);


--
-- Name: campaigns campaigns_marketer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_marketer_id_fkey FOREIGN KEY (marketer_id) REFERENCES public.marketers(marketer_id);


--
-- Name: customers customers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: marketers marketers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.marketers
    ADD CONSTRAINT marketers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: marketing_materials marketing_materials_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.marketing_materials
    ADD CONSTRAINT marketing_materials_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(campaign_id) ON DELETE CASCADE;


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: marketing_service
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


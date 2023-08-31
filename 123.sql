--
-- PostgreSQL database dump
--

-- Dumped from database version 13.11
-- Dumped by pg_dump version 13.11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: AgeRestriction; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."AgeRestriction" AS ENUM (
    'Age',
    'Kids',
    'Children',
    'Body',
    'Big'
);


ALTER TYPE public."AgeRestriction" OWNER TO postgres;

--
-- Name: TypeOfAuthor; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."TypeOfAuthor" AS ENUM (
    'DIRECTOR',
    'PRODUCER',
    'DIRECTOR_PRODUCER',
    'ACTOR',
    'OPERATOR',
    'ART',
    'ART_LOOK',
    'COMPOSER',
    'AUTHOR',
    'ASSISTANT_PRODUCER',
    'ASSISTANT_OPERATOR',
    'GRIM',
    'SOUND',
    'VISUAL_EFFECTS',
    'GAFER',
    'PHOTO',
    'HELP_PRODUCER',
    'MAIN_ACTOR',
    'HELP_OPERATOR',
    'ART_OPERATOR',
    'WEAR_OPERATOR',
    'HELP_AUTHOR'
);


ALTER TYPE public."TypeOfAuthor" OWNER TO postgres;

--
-- Name: TypeOfFilm; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public."TypeOfFilm" AS ENUM (
    'COMEDY',
    'DRAMA',
    'FANTASY',
    'HORROR',
    'TRILLER',
    'STUDY',
    'MELODRAMMA',
    'MULT',
    'WEB',
    'DOC'
);


ALTER TYPE public."TypeOfFilm" OWNER TO postgres;

--
-- Name: change_mark(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.change_mark() RETURNS void
    LANGUAGE plpgsql
    AS $$
    DECLARE 
		film_id_to_change UUID;
		ratingSum numeric;
		x UUID[];
	BEGIN
		x := ARRAY (SELECT "Film".film_id FROM "Film"); 
		FOREACH film_id_to_change IN ARRAY x
    	LOOP
			select sum(rating)/count(rating) into ratingSum from "ratingUser" where film_id_to_change = film_id;
			IF ratingSum IS NULL
			THEN
    			ratingSum := 0;
			END IF;
			
			update "Film" set rating = ratingSum where "Film".film_id = film_id_to_change;
        END LOOP ;
    END;
$$;


ALTER FUNCTION public.change_mark() OWNER TO postgres;

--
-- Name: check_mark(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.check_mark() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE 
		ratingSum numeric;
	BEGIN
		ratingSum := 0.0;
        --
        -- Добавление строки в emp_audit, которая отражает операцию, выполняемую в emp;
        -- для определения типа операции применяется специальная переменная TG_OP.
        --
        IF (TG_OP = 'INSERT') THEN
			select sum(rating)/count(rating) into ratingSum from ratingUser where film_id = NEW.film_id;
            update Film set rating = ratingSum where film_id = NEW.film_id ;
        END IF;
        RETURN NULL; -- возвращаемое значение для триггера AFTER игнорируется
    END;
$$;


ALTER FUNCTION public.check_mark() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Comment" (
    comment_id uuid NOT NULL,
    film_id uuid NOT NULL,
    from_id uuid NOT NULL,
    to_id uuid,
    date_add date NOT NULL,
    data text NOT NULL
);


ALTER TABLE public."Comment" OWNER TO postgres;

--
-- Name: Fest_AD; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Fest_AD" (
    fest_id uuid NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    news_or_ad boolean NOT NULL
);


ALTER TABLE public."Fest_AD" OWNER TO postgres;

--
-- Name: Film; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Film" (
    film_id uuid NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    url text NOT NULL,
    rating double precision NOT NULL,
    type_of_film public."TypeOfFilm" NOT NULL,
    data_create date NOT NULL,
    data_add date NOT NULL,
    age_restriction public."AgeRestriction" NOT NULL
);


ALTER TABLE public."Film" OWNER TO postgres;

--
-- Name: News_Ad; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."News_Ad" (
    news_id uuid NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    news_or_ad boolean NOT NULL
);


ALTER TABLE public."News_Ad" OWNER TO postgres;

--
-- Name: author; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.author (
    author_id uuid NOT NULL,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL,
    type public."TypeOfAuthor" NOT NULL
);


ALTER TABLE public.author OWNER TO postgres;

--
-- Name: authorAbout; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."authorAbout" (
    user_id uuid NOT NULL,
    about_person text,
    about_awards text
);


ALTER TABLE public."authorAbout" OWNER TO postgres;

--
-- Name: bookmarkUser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."bookmarkUser" (
    mark_id uuid NOT NULL,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL
);


ALTER TABLE public."bookmarkUser" OWNER TO postgres;

--
-- Name: countViewFilm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."countViewFilm" (
    hist_view_id uuid NOT NULL,
    film_id uuid NOT NULL,
    count integer NOT NULL
);


ALTER TABLE public."countViewFilm" OWNER TO postgres;

--
-- Name: historyViewUser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."historyViewUser" (
    hist_id uuid NOT NULL,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL
);


ALTER TABLE public."historyViewUser" OWNER TO postgres;

--
-- Name: notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification (
    not_id uuid NOT NULL,
    user_id uuid NOT NULL,
    description uuid NOT NULL,
    is_view boolean NOT NULL,
    date date NOT NULL
);


ALTER TABLE public.notification OWNER TO postgres;

--
-- Name: ratingUser; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ratingUser" (
    rating_id uuid NOT NULL,
    film_id uuid NOT NULL,
    user_id uuid NOT NULL,
    rating numeric NOT NULL
);


ALTER TABLE public."ratingUser" OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    name text NOT NULL,
    surname text NOT NULL,
    login text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    "dataBirthday" date NOT NULL,
    is_author boolean NOT NULL,
    path_to_image text,
    is_active boolean NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: Comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Comment" (comment_id, film_id, from_id, to_id, date_add, data) FROM stdin;
\.


--
-- Data for Name: Fest_AD; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Fest_AD" (fest_id, title, description, news_or_ad) FROM stdin;
\.


--
-- Data for Name: Film; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Film" (film_id, name, description, url, rating, type_of_film, data_create, data_add, age_restriction) FROM stdin;
38b8878b-500b-4da9-8f17-de0eb6a6b2db	Интрига	к.м.фильм "Интрига", 21мин, 2023г. В главных ролях Дарья Чередникова, Кирилл Кривошеев. Режиссер Дмитрий Шиковец	https://www.youtube.com/embed/szOksOltkbY	0	DRAMA	2023-01-01	2023-08-28	Children
305cc75b-ee1e-4aea-949d-47dd11756558	Вер(т)ность	Студенческая работа "немые этюды".  Верность через призму "вертности".  Реакция интровертов и экстравертов на одну и ту же ситуацию.	https://rutube.ru/play/embed/private/802a2795858ebbb34d86191a7afc712a/?p=y7Ff8J8aHOnNo-okkmC02Q	0	STUDY	2022-01-01	2023-08-28	Children
\.


--
-- Data for Name: News_Ad; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."News_Ad" (news_id, title, description, news_or_ad) FROM stdin;
e82c1dfb-32f7-41d3-91b4-52a641028712	День рождения Донатеатра в День российского кино!	 День российского кинематографиста - праздник, который ежегодно отмечается 27 августа. Этот день посвящен всем творческим людям, работающим в киноиндустрии, которые создают и развивают отечественное кино. В этот важный праздник, мы открываем онлайн-платформу которая  позволяет всем отдать должное их таланту и достижениям.	t
f35e1ce6-358c-403a-b6bd-d6adf670924b	Закрытый показ 	 ПРЕСС-РЕЛИЗ\n\nЗакрытый показ к.м. фильма «Интрига» в самом атмосферном кинотеатре Калининграда.\n\n28 августа 2023г в 19:00 в кинотеатре Заря состоится закрытый показ короткометражного фильма «Интрига». Это дебютная работа калининградского режиссера Дмитрия Шиковца. \n\nПриглашаем региональные СМИ присоединиться к нам и поддержать калининградские творческие инициативы.\n\nФормат мероприятия предусматривает показ фильма в кинозале, знакомство с участниками съемочной группы. После чего в фойе кинотеатра предусмотрено общение и обсуждение. \n\nМесто проведения: кинотеатр Заря, улица Проспект Мира, 41-43, Калининград.\nДата и время: 21 августа 2023 года, 19:00.\n\nНеобходима предварительная регистрация:\nEmail: illusionofff@yandex.ru\nСообщество ВКонтакте: https://vk.com/public219307257\n\nМы будем рады видеть вас на закрытом показе фильма "Интрига" и с нетерпением ждем вашей поддержки и внимания!\n\nКонтактное лицо:\nДмитрий Шиковец \nТелефон: +7 9062195379\nEmail: illusionofff@yandex.ru\n	t
\.


--
-- Data for Name: author; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.author (author_id, user_id, film_id, type) FROM stdin;
679d06fa-5d2a-4694-9510-4dfa2f22153a	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62	DIRECTOR
869c9681-85cd-44f5-b4a4-54c1a7fe2cc0	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62	HELP_OPERATOR
15f80099-bb0f-45d7-99d6-64a79baeb038	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db	DIRECTOR
3fb287b7-7e02-4268-be41-7e554a76ca01	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	a41e1247-01a8-463c-8e9c-69f443669f19	DIRECTOR
495dd3ff-4ee4-4dfc-9923-6cb6ef5fda63	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558	DIRECTOR
\.


--
-- Data for Name: authorAbout; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."authorAbout" (user_id, about_person, about_awards) FROM stdin;
89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	Андрей крутой	первый писька на районе; член огромной
\.


--
-- Data for Name: bookmarkUser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."bookmarkUser" (mark_id, user_id, film_id) FROM stdin;
\.


--
-- Data for Name: countViewFilm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."countViewFilm" (hist_view_id, film_id, count) FROM stdin;
7d4b3fd7-af7d-4e69-ad8b-577a1a968549	1432f43a-a99a-4e6b-82bc-3a862292fa5f	8
e786fe5b-48d4-4497-824d-cd5b682d8e4e	e29dbbe5-aa42-4c74-b7a1-39b97a7980d9	1
dccab944-1f98-4e1f-8033-181707fa3568	3e3750e4-34bb-4995-850e-b7bbcc2ab601	4
f4e3971c-8edd-4214-b641-36b3c3c3cae5	9d406001-cfc4-4f0c-9a18-507f86399a8b	2
fc349363-3aa1-49e9-bc01-037f2100e373	2c83d72c-5dc0-4531-86d6-4b047f4f47b4	9
4ca35e45-3a5f-4c60-b47a-5b7fb0ba2d60	94967fc9-cdea-4689-9b00-7dcd0014691f	3
95bd823d-bc90-4d9a-a455-a7285946cd8f	8be6464e-efd1-4bcd-8ba6-02f282e85275	36
895cc382-017a-454a-9e1f-69e1dca23c5a	2c41fa48-4c71-4c5a-82a2-d6f9fec0a9c6	1
05b71518-15fe-4f23-a3fa-e1d710730cba	4c1897a4-3682-4203-b15d-acab2f25ec4a	28
73292580-8897-4767-9421-e40ae2640a95	ec97737d-6ffe-4b0b-9ac4-95a8f790cec8	5
158cf0fb-f364-428e-b867-88f0e2834512	f077ecb1-0447-4eaf-bde2-9b512a36d73e	125
aa986b12-1054-4af8-969d-f20b39ff7cbc	b2b8b929-4f6d-4d03-8d0d-a0bdfc7f4764	11
d7546a2e-49c1-4aeb-ab91-300da0f4117a	0a6f34e7-6173-4c93-8bfd-13dabce64bf1	11
c121e943-9742-4529-b632-7914d5a7c998	d1a71f78-9da9-4243-a19f-72fb3b529976	36
0e00d70e-2106-42e4-b53a-16b50df356bf	816e7dbe-0636-4fb0-b718-94d0e9874d62	4
3d5c3554-c793-4428-9a2c-e536e64b13fb	abd98940-f6aa-4df4-b688-b2b53ccb2847	28
3ecdd212-4a94-4ab7-b7de-795330adb798	6a900cf1-49f5-4ae8-9540-1463ef033d9c	1
7c570bba-b8b8-49b1-990e-1bdb6f9605ba	15632316-1aab-4df8-8897-676b26ebb7e3	183
0f05a98b-8143-4db8-bf0f-00815111e011	5f1a331c-41c7-43a2-a404-4fcb729e9049	8
ab77650e-dd52-4cb5-9022-1401f80cf681	a41e1247-01a8-463c-8e9c-69f443669f19	1
415f5e4a-f82c-4b5a-b9b0-ecaebe0a2e8e	636121f4-11f9-491e-95a2-e083148e3709	2
5836687d-e647-412d-ad70-7a76b3bbdc13	38b8878b-500b-4da9-8f17-de0eb6a6b2db	74
03601bbc-171e-4646-a6a9-c1b338b6e36f	305cc75b-ee1e-4aea-949d-47dd11756558	15
\.


--
-- Data for Name: historyViewUser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."historyViewUser" (hist_id, user_id, film_id) FROM stdin;
3e128b37-ba98-45f5-8e34-b856436b6c55	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62
c2dbf917-5a8e-41f1-8572-a574bd5f7e4e	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62
dc2de08e-74c5-4a46-9494-1dee08941c23	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62
9dd5376e-eee5-4ce9-9216-957f167be6cb	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62
04fe4b2c-7394-4382-b27e-06f6998d1181	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	816e7dbe-0636-4fb0-b718-94d0e9874d62
9aa86d4d-dfe4-4357-a79a-5e418167a53b	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
9da2af6f-f4f6-4fe1-b999-ecd6169af49e	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
09369772-cd59-4dcd-9f26-b27c5ce04a5b	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
0a9df5f6-4f47-46e1-b749-8099f6694723	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	a41e1247-01a8-463c-8e9c-69f443669f19
1ef57d8a-2abf-444a-933b-03a46dd0d05c	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	a41e1247-01a8-463c-8e9c-69f443669f19
44e8be9c-254f-42e0-9c2b-f248a469e566	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	38b8878b-500b-4da9-8f17-de0eb6a6b2db
385f4e29-94f7-4165-81fa-d5c8521e2a63	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	38b8878b-500b-4da9-8f17-de0eb6a6b2db
a4dd57ce-c3a5-4281-bfae-12e7bf2d81f7	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	38b8878b-500b-4da9-8f17-de0eb6a6b2db
ce27b821-1191-4aef-9c19-4144bc1024c9	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	38b8878b-500b-4da9-8f17-de0eb6a6b2db
fa0639a5-c189-45c0-b997-4bce91b891be	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
c1590a56-c7b4-4873-8834-cb8dbcade58b	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
11cd3725-e8d4-473f-8a10-5206958c71c9	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
f18a0510-0bf3-483e-9508-ca1f12acaa30	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
5d7fe114-852f-435b-b42f-12fe3e1d4541	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
57deebc4-187d-42e3-8b34-997f1f701bbe	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
b79f4b9e-b6c4-4635-a886-15a16e8fbd6e	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
5cf7bf4c-aa28-473f-8271-5a12d504e483	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
c8d7124b-c136-46dc-a53d-4622a2ef1380	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
8841b137-8ba7-43ef-a5c7-5fd42380fe1d	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
7a429c2c-7c0b-41a8-b9b2-10f9083560b5	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
fd9da48c-be58-4ee0-a34d-43ad6bd9f58e	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
7bf00c0d-3e38-48d4-a206-2c2441d83b68	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
b08e5c1a-49b3-4f07-b221-c813d664e601	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
0c048393-de2b-4db1-bfa5-4965f1c148a9	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
83441e5d-cc1e-4032-809e-9b59bf0a6a54	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
f3da0b29-df33-43e2-8d8d-ad4c3ed7fe95	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
5a3f38e2-e9da-4846-b97d-bb92a8aff015	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
3da73a6b-69a0-4f99-a973-c4d349b90ffa	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
fbb63b48-8f37-4e55-8aa5-6b4ecb9c8090	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
85eb690d-5821-4bb5-a44d-2ff3d5c3a8fd	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
7eae3433-7ff6-4601-8769-ac8838d73ed0	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
7fc6f410-f99b-49da-b2ed-090fc97035ff	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
30c93a5a-205a-48b8-a3d9-04e5d6e618f3	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
c0a27d87-3180-416b-b47a-3e523d25d23a	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
c915addc-8f88-42db-ab47-6a33045bab80	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
baebafad-232a-4608-be6e-905a4a485d34	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
1365222a-d87d-4e88-a017-e2f27c8ed854	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
bdecb76c-c179-414c-bfae-8dd2bf4eb454	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
29a150ca-e2ef-4854-8cdf-7a5d4342db0a	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
d1e856b4-ec77-4627-ad7f-983989b0876b	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
d7cadd7c-bcad-4494-b1dd-3fc823bd3b48	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
cb515c32-8d4a-4c57-8bea-4f7ffe50fade	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
8827f86e-7dd7-4d86-9c16-e307c8ff4fd6	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
b90972f4-8408-4c80-b62d-0ac31af3b4db	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
cc7d4382-de96-4d6d-ac7d-81671e1fe69d	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
202a412a-997d-422f-a358-cea5b7ac6c84	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
eb647fcf-b378-4574-bbff-0b13b0bc50b4	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
f405d460-6cfc-4be5-bc9d-55d62e597012	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
0c632ebb-af06-487d-94cb-9a9ad7deedaf	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
fc78fe62-b7ac-4163-bd6e-b2901be1444a	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
a9d08beb-9778-486f-8504-a42f9a9a728b	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
93695757-a7db-4ee6-9216-0f20f57f39b6	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
ee0872c0-488f-41b9-9dec-ec5df55c9724	d2c1157b-a61a-48a0-9f0b-b09de589a52e	38b8878b-500b-4da9-8f17-de0eb6a6b2db
9b80a3aa-9752-4939-9ac5-f2ed146ce729	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
959a15a9-a8e4-4422-be19-17647a26dc75	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
b7c575b0-8779-4e63-a8f0-8009d6dc4243	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
060b5bad-305b-4ef0-9746-e7b09bfe976e	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
9b96927e-c360-499c-ade5-05afe8fb4769	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
3b34a1cd-2b81-48c7-9a10-4c75a1725002	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
bdb80269-0b64-444b-9395-f27778d557c0	26175185-37ad-4f7a-9c2e-08c3754d51ce	38b8878b-500b-4da9-8f17-de0eb6a6b2db
17fd0d55-2ab9-4aee-852b-95ac53e533d1	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
9a4c8b6c-f44e-479d-a1a0-eb661cffef96	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
ea3e7cf3-2e5c-47ae-8bdc-94131f27b6a8	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
bdca6cb9-63a1-4c90-be58-bb5061389fe2	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
ab70f858-6917-4e5c-8248-4a5441e10a5d	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
66d975b3-51f0-43e8-bb23-89b299e665e2	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
762bc474-3ff4-4f7d-9ce0-b7670e48e3ea	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
525402c4-305b-446a-93cb-041558145c08	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
26c9d428-2bf5-46a7-a177-953d3bda0a35	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
d0c17c00-00d9-4f5f-a91d-8e93ddf7d061	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
b93bbaff-be00-41fb-9a41-5ce7d2795594	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
e3444fca-dac7-445b-a89f-61d7024454ff	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
5ea3de25-f06b-4d49-bc75-dd8c9e200084	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
daa895cd-ee0a-41cc-b4a5-754b53f86cbd	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
67f04f43-9395-4619-9ffa-fb5c13031cf4	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
e2dab5d8-4a4c-4f18-96e6-d7d4455dbd2d	d8094dc5-e8a8-443e-a272-96d4b7508b65	305cc75b-ee1e-4aea-949d-47dd11756558
df431c30-25c9-434b-9122-85ac40e55939	d8094dc5-e8a8-443e-a272-96d4b7508b65	38b8878b-500b-4da9-8f17-de0eb6a6b2db
\.


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification (not_id, user_id, description, is_view, date) FROM stdin;
\.


--
-- Data for Name: ratingUser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."ratingUser" (rating_id, film_id, user_id, rating) FROM stdin;
ee0f9aec-ff45-4c62-9b77-869a9fcf757b	816e7dbe-0636-4fb0-b718-94d0e9874d62	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	2
0569e71e-7f40-4d1c-9aac-ce731e86aec0	38b8878b-500b-4da9-8f17-de0eb6a6b2db	89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	5
61604dac-61fe-4b69-800b-b3e2c599da1f	38b8878b-500b-4da9-8f17-de0eb6a6b2db	d2c1157b-a61a-48a0-9f0b-b09de589a52e	4
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, name, surname, login, email, password, "dataBirthday", is_author, path_to_image, is_active) FROM stdin;
f79f39d4-e4c8-4e7f-ba7d-050fe75395c2	выфвфы	выфвыф	dasdsadas	pkulbaka@mail.ru	$2b$12$yOlm8YNLYFn.IWJQrgTO7uE3cdaPOSqxAro.IhOlEHQi4ZOtN32y2	2000-07-08	f	 	f
85d1373e-48cf-4550-8dff-50a0dc5a8e95	выфвфы	вфыв	ad	dsd@mail.ru	$2b$12$/i2b2gJV5NPoZGkZBL25/OpX5BYqOrmmUQmDaaLsFW7SYMnDc8Ei2	2000-07-08	f	 	f
25bba9e8-cfee-448a-8085-02ee44e3ef9f	Антон	Рег	anton	forworkantonov2020@gmail.com	$2b$12$IGOn3k8UbfQgA00C3mIxYeYXpygl29UxyPxUnx67OQjakkBaXa/Ju	2000-07-08	f	 	t
89edcfdf-9763-4a9b-883b-b7b7bb52b6b4	Павел	Кульбака	Dsada	forworkkul2000pi@yandex.ru	$2b$12$fYyjT4sQvbEfJEY8FsyP9.gDBpgYJz2pT.4cor9bsLXAg6myFVqhy	2000-07-08	t	 	t
d8094dc5-e8a8-443e-a272-96d4b7508b65	Дмитрий	Шиковец	illusionOff	shikovets71@yandex.ru	$2b$12$iiHR/eoQcQFeVcj9hGbcNe9xxWUpJBO2LEmMf667dtrns9hdCF0AO	1971-05-10	t	 	t
26175185-37ad-4f7a-9c2e-08c3754d51ce	Кирилл	Кривошеев	Kirill1980	ki_ru_ll@mail.ru	$2b$12$V2A23AUJQTk4qB2AKq.Up.RBOFUydQj5A1XasOe7S3NlyiiwFtk2G	1980-09-05	f	 	t
d2c1157b-a61a-48a0-9f0b-b09de589a52e	Артур	Фетисов	ArthurFetis0v	arthurkremator@gmail.com	$2b$12$VAt6F6gy2ZLv5GAfzvE0tufwE2FxyQvKSifPfDgsXuKaFtGOpzvx2	1970-02-13	f	 	t
\.


--
-- Name: Comment Comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Comment"
    ADD CONSTRAINT "Comment_pkey" PRIMARY KEY (comment_id);


--
-- Name: Fest_AD Fest_AD_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Fest_AD"
    ADD CONSTRAINT "Fest_AD_pkey" PRIMARY KEY (fest_id);


--
-- Name: Film Film_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Film"
    ADD CONSTRAINT "Film_pkey" PRIMARY KEY (film_id);


--
-- Name: News_Ad News_Ad_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."News_Ad"
    ADD CONSTRAINT "News_Ad_pkey" PRIMARY KEY (news_id);


--
-- Name: authorAbout authorAbout_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."authorAbout"
    ADD CONSTRAINT "authorAbout_pkey" PRIMARY KEY (user_id);


--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (author_id);


--
-- Name: bookmarkUser bookmarkUser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."bookmarkUser"
    ADD CONSTRAINT "bookmarkUser_pkey" PRIMARY KEY (mark_id);


--
-- Name: countViewFilm countViewFilm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."countViewFilm"
    ADD CONSTRAINT "countViewFilm_pkey" PRIMARY KEY (hist_view_id);


--
-- Name: historyViewUser historyViewUser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."historyViewUser"
    ADD CONSTRAINT "historyViewUser_pkey" PRIMARY KEY (hist_id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (not_id);


--
-- Name: ratingUser ratingUser_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ratingUser"
    ADD CONSTRAINT "ratingUser_pkey" PRIMARY KEY (rating_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- PostgreSQL database dump complete
--


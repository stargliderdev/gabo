create schema public;

comment on schema public is 'standard public schema';

alter schema public owner to postgres;

create sequence author_authorid_seq;

alter sequence author_authorid_seq owner to sysdba;

create sequence generoid_seq;

alter sequence generoid_seq owner to sysdba;

create sequence statusid_seq;

alter sequence statusid_seq owner to root;

create sequence tags_ta_id_seq
	maxvalue 2147483647;

alter sequence tags_ta_id_seq owner to root;

create table if not exists authors
(
	au_id integer default nextval('author_authorid_seq'::regclass) not null
		constraint authors_pk
			primary key,
	au_name varchar(150) not null,
	pu_type integer default 101 not null
);

alter table authors owner to sysdba;

create table if not exists genero
(
	ge_id integer default nextval('generoid_seq'::regclass) not null
		constraint genero_pk
			primary key,
	ge_title varchar(100) not null,
	ge_electronic boolean default false not null
);

alter table genero owner to sysdba;

create table if not exists livros
(
	pu_id serial not null
		constraint livros_pk
			primary key,
	pu_subject integer default 1,
	pu_title varchar(100),
	pu_translator varchar(60),
	pu_edition_number integer default 0,
	pu_ed_local varchar(40),
	pu_ed_date varchar(50),
	pu_volumes integer default 0,
	pu_isbn varchar(25),
	pu_cota varchar(10),
	pu_obs text,
	pu_collection integer default 1 not null,
	pu_author_others varchar(150),
	pu_type smallint default 101 not null,
	pu_tags varchar(1024),
	pu_language integer default 1 not null,
	pu_volume integer default 1 not null,
	pu_pages integer default 0,
	pu_media integer default 1 not null,
	pu_genero integer default 1 not null,
	pu_author_id integer default 0 not null,
	pu_sub_title varchar(255),
	pu_collection_number integer default 1,
	pu_title_original varchar(100),
	pu_lang integer default 1 not null,
	pu_status integer default 1 not null,
	pu_media_format integer default 1 not null,
	pu_editor_id integer default 1 not null,
	pu_isbn10 varchar(10),
	pu_deplegal varchar(20),
	pu_origem varchar(30),
	pu_estado_fisico varchar(10) default 'Novo'::character varying,
	pu_sinopse text,
	pu_ed_year smallint
);

alter table livros owner to sysdba;

create table if not exists tag_ref
(
	id serial not null
		constraint tag_ref_pkey
			primary key,
	tr_book integer not null,
	tr_tag integer not null
);

alter table tag_ref owner to root;

create table if not exists status
(
	st_id integer default nextval('statusid_seq'::regclass) not null
		constraint status_pk
			primary key,
	st_nome varchar(80),
	pu_type integer default 101 not null
);

alter table status owner to sysdba;

create table if not exists tags
(
	ta_id integer default nextval(('public.tags_ta_id_seq'::text)::regclass) not null
		constraint tags_pkey
			primary key,
	ta_name varchar(60) not null
		constraint tags_ta_name_key
			unique
);

alter table tags owner to root;

create table if not exists types
(
	ty_id integer not null
		constraint types_pk
			primary key,
	ty_name varchar(80),
	ty_enable integer default 1 not null
);

alter table types owner to sysdba;

create table if not exists params
(
	param_key varchar(20) not null
		constraint params_pkey
			primary key,
	param_data text
);

alter table params owner to root;

create unique index params_param_key_uindex
	on params (param_key);

create or replace view or_tags(tr_book, tr_tag) as
SELECT tag_ref.tr_book,
       tag_ref.tr_tag
FROM tag_ref
WHERE ((tag_ref.tr_tag = 277) OR (tag_ref.tr_tag = 397));

alter table or_tags owner to root;


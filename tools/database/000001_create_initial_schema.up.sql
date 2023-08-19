create extension if not exists "uuid-ossp";

create table if not exists characters(
    id uuid not null 
        constraint pk_characters_id primary key
        constraint df_characters_id default uuid_generate_v4(),
    name varchar(244) not null,
    from_where varchar(244) not null
);

copy characters (id, name, from_where)
    from '/database/fixtures/character.csv'
    delimiter ';' csv header;
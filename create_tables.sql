CREATE TABLE products
(
    id              serial      NOT NULL,
    name            varchar     NOT NULL,
    price           int         NOT NULL,
    description     text,
    quantity        int         NOT NULL,

    CONSTRAINT products_pkey PRIMARY KEY (id)
);

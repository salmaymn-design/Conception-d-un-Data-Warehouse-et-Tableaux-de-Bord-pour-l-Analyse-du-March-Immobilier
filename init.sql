DROP TABLE IF EXISTS staging.staging_darkom;

CREATE TABLE staging.staging_darkom (
    annonce_id TEXT,
    date_publication TEXT,
    titre TEXT,
    ville TEXT,
    quartier TEXT,
    type_bien TEXT,
    transaction TEXT,
    prix TEXT,
    surface TEXT,
    nb_chambres TEXT,
    nb_salles_bain TEXT,
    etage TEXT,
    annee_construction TEXT
);




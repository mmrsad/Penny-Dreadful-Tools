CREATE TABLE IF NOT EXISTS deck_archetype_change (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    changed_date INT NOT NULL,
    deck_id INT NOT NULL,
    archetype_id INT NOT NULL,
    person_id INT NOT NULL,
    FOREIGN KEY(deck_id) REFERENCES deck(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(archetype_id) REFERENCES archetype(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(person_id) REFERENCES person(id) ON UPDATE CASCADE ON DELETE CASCADE
);


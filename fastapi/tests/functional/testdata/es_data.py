import uuid

es_data_for_tests_film = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "directors_names": ["Stan"],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "directors": [
            {"id": "111", "name": "Ann"},
            {"id": "222", "name": "Bob"},
        ],
        "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
    }
    for _ in range(60)
]

es_data_for_tests_genre = [
    {
        "id": str(uuid.uuid4()),
        "name": "comedy",
        "description": "comedy genre description",
    }
    for _ in range(10)
]

es_data_person_by_id_index = [
    {
        "id": "5f1a4219-b533-489f-8af2-992692504999",
        "full_name": "Ann Brown",
        "films": [
            "5f1a4219-b533-489f-8af2-0d2692504857",
            "e95044a7-1f66-4164-9650-3bf2132d7119",
        ],
    }
]

es_data_films_for_persons = [
    {
        "id": film_id,
        "imdb_rating": 8.5,
        "genre": ["Action", "Sci-Fi"],
        "title": "The Star",
        "description": "New World",
        "directors_names": ["Stan"],
        "actors_names": ["Ann Brown", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "directors": [
            {"id": "111", "name": "Ann"},
            {"id": "222", "name": "Bob"},
        ],
        "actors": [
            {"id": "5f1a4219-b533-489f-8af2-992692504999", "name": "Ann Brown"},
            {"id": "222", "name": "Bob"},
        ],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
    }
    for film_id in [
        "5f1a4219-b533-489f-8af2-0d2692504857",
        "e95044a7-1f66-4164-9650-3bf2132d7119",
    ]
]


class Persons:
    from faker import Faker

    fake = Faker()

    def __init__(self, number: int = 100):
        self.number = number

    def get_es_data_persons(self):
        self.persons = [
            {
                "id": str(uuid.uuid4()),
                "full_name": self.fake.first_name() + " " + self.fake.last_name(),
                "films": [str(uuid.uuid4())],
            }
            for _ in range(self.number)
        ]
        return self.persons

    def get_es_data_persons_films(self):
        self.films = [
            {
                "id": person["films"][0],
                "imdb_rating": 8.5,
                "genre": ["Action", "Sci-Fi"],
                "title": "The Star",
                "description": "New World",
                "directors_names": ["Stan"],
                "actors_names": [person["full_name"], "Bob"],
                "writers_names": ["Ben", "Howard"],
                "directors": [
                    {"id": "111", "name": "Ann"},
                    {"id": "222", "name": "Bob"},
                ],
                "actors": [
                    {"id": person["id"], "name": person["full_name"]},
                    {"id": "222", "name": "Bob"},
                ],
                "writers": [
                    {"id": "333", "name": "Ben"},
                    {"id": "444", "name": "Howard"},
                ],
            }
            for person in self.persons
        ]

        return self.films

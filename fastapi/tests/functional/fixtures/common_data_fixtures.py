import pytest


@pytest.fixture
def person_id():
    return "5f1a4219-b533-489f-8af2-992692504999"


@pytest.fixture
async def persons_expected_answer(person_id):
    return {
        "films": [
            {"roles": ["actor"], "uuid": "5f1a4219-b533-489f-8af2-0d2692504857"},
            {"roles": ["actor"], "uuid": "e95044a7-1f66-4164-9650-3bf2132d7119"},
        ],
        "full_name": "Ann Brown",
        "uuid": person_id,
    }

import sys

sys.path.append('..')

import pytest
from api.db.settings import engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="module", autouse=True)
def get_session():
    '''Fixture to prepare database session to be used in tests.'''
    with Session(engine) as session:
        yield session
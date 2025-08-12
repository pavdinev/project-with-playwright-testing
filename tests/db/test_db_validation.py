import pytest
from utils.db_helpers import initialize_db, insert_booking, fetch_booking

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    initialize_db()
    yield
    # Optionally: cleanup after tests if needed

def test_insert_and_fetch_booking():
    insert_booking("John Doe", "2025-01-01")
    record = fetch_booking("John Doe")
    assert record is not None
    assert record[1] == "John Doe"
    assert record[2] == "2025-01-01"

import json

import pytest

from app import create_app

VALID = {
    "name": "Mahreen Malik",
    "reg_no": "FA23-BSE-006",
    "title": "Lab Midterm",
    "url": "https://github.com/YourUsername/assignment-portal",
}

@pytest.fixture
def setup(tmp_path):
    data_file = tmp_path / "submissions.json"
    app = create_app(str(data_file))
    app.config["TESTING"] = True
    return app.test_client(), data_file

def test_valid_submission_is_saved_and_listed(setup):
    client, data_file = setup
    response = client.post("/", data=VALID)
    assert response.status_code == 200
assert "INTENTIONALLY_WRONG_MESSAGE" in response.get_data(as_text=True)
    page = client.get("/").get_data(as_text=True)
    assert VALID["reg_no"] in page
    assert "Lab Midterm" in page
    assert len(json.loads(data_file.read_text())) == 1

def test_missing_registration_number_is_rejected(setup):
    client, data_file = setup
    response = client.post("/", data={**VALID, "reg_no": ""})
    assert response.status_code == 400
    assert "Registration number is required" in response.get_data(as_text=True)
    assert not data_file.exists()

def test_invalid_url_is_rejected_and_not_saved(setup):
    client, data_file = setup
    response = client.post("/", data={**VALID, "url": "not-a-valid-url"})
    assert response.status_code == 400
    assert "Submission URL is invalid" in response.get_data(as_text=True)
    assert not data_file.exists()
from project_tool import responses

# BLACK-BOX (Equivalent Partitioning): partition {success without data} should produce correct response schema.
def test_success_without_data_has_expected_shape():
    resp = responses.success("OK")
    assert isinstance(resp, dict)
    assert resp["success"] is True
    assert resp["message"] == "OK"
    assert "data" not in resp

# BLACK-BOX (Equivalent Partitioning): partition {success with data} should include "data" field unchanged.
def test_success_with_data_includes_data():
    payload = {"x": 1}
    resp = responses.success("OK", data=payload)

    assert resp["success"] is True
    assert resp["message"] == "OK"
    assert resp["data"] == payload

# BLACK-BOX (Equivalent Partitioning): partition {error response} should produce correct error schema.
def test_error_has_expected_shape():
    resp = responses.error("Bad")

    assert isinstance(resp, dict)
    assert resp["success"] is False
    assert resp["message"] == "Bad"
    assert "data" not in resp

# BLACK-BOX (Equivalent Partitioning): partition {created response} should contain ID and success flag.
def test_project_created_message_and_success_flag():
    resp = responses.project_created("P-ABC123")

    assert resp["success"] is True
    assert "created successfully" in resp["message"].lower()
    assert "P-ABC123" in resp["message"]

# BLACK-BOX (Equivalent Partitioning): partition {updated response} should contain field name, ID, and success flag.
def test_project_updated_message_and_success_flag():
    resp = responses.project_updated("P-ABC123", "title")

    assert resp["success"] is True
    msg = resp["message"].lower()
    assert "updated" in msg
    assert "title" in msg
    assert "P-ABC123" in resp["message"]

# BLACK-BOX (Equivalent Partitioning): partition {deleted response} should contain ID and success flag.
def test_project_deleted_message_and_success_flag():
    resp = responses.project_deleted("P-ABC123")

    assert resp["success"] is True
    assert "deleted successfully" in resp["message"].lower()
    assert "P-ABC123" in resp["message"]

# BLACK-BOX (Equivalent Partitioning): partition {not found} should contain error flag and ID.
def test_project_not_found_message_and_error_flag():
    resp = responses.project_not_found("P-NOTREAL")

    assert resp["success"] is False
    assert "not found" in resp["message"].lower()
    assert "P-NOTREAL" in resp["message"]

# BLACK-BOX (Equivalent Partitioning): partition {invalid input} should prefix message correctly and set error flag.
def test_invalid_input_message_and_error_flag():
    resp = responses.invalid_input("Something wrong")

    assert resp["success"] is False
    msg = resp["message"].lower()
    assert msg.startswith("invalid input:")
    assert "something wrong" in msg

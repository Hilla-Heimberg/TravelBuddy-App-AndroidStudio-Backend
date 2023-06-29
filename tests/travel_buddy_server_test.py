import json
import requests
import unittest

from models.SectionContent import SectionContent

GET_ENDPOINT = \
    "https://7dzu681lzl.execute-api.us-west-2.amazonaws.com/default/travel-buddy-section-content-getter-lambda"
PUT_ENDPOINT = \
    "https://7dzu681lzl.execute-api.us-west-2.amazonaws.com/default/travel-buddy-section-content-uploader-lambda"

USER_ID1 = "user1234"
USER_ID2 = "user5678"
SECTION1 = "Flights"
SECTION2 = "Food_and_Drinks"
SECTION1_CONTENT1 = "Air France 962 from TLV to CDG"
SECTION1_CONTENT2 = "Finnair 666 from CPH to HEL"
SECTION2_CONTENT1 = "McDonalds McNuggets and fries"

GET_REQUEST_PARAMS1 = {"userId": USER_ID1, "section": SECTION1}
GET_REQUEST_PARAMS1_NON_EXISTING_SECTION = {"userId": USER_ID1, "section": SECTION2}
GET_REQUEST_MISSING_PARAMS1 = {"userId": USER_ID1}
GET_REQUEST_PARAMS_NON_EXISTING_USER = {"userId": USER_ID2, "section": SECTION1}

PUT_REQUEST_PARAMS1 = {"userId": USER_ID1, "section": SECTION1, "content": SECTION1_CONTENT2}
PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION = {"userId": USER_ID1, "section": SECTION2, "content": SECTION2_CONTENT1}
PUT_REQUEST_PARAMS1_NON_EXISTING_USER = {"userId": USER_ID2, "section": SECTION2, "content": SECTION2_CONTENT1}
PUT_REQUEST_MISSING_PARAMS1 = {"userId": USER_ID1, "section": SECTION1}


class TestSocialProfileServerEndpoints(unittest.TestCase):

    def setUp(self):
        # Add test entry {"user1234", {"Flights": "Air France 962 from TLV to CDG"}}
        test_entry = SectionContent(USER_ID1)
        setattr(test_entry, SECTION1, SECTION1_CONTENT1)
        test_entry.save()

    def tearDown(self):
        # Remove test entries
        for userId in [USER_ID1, USER_ID2]:
            if SectionContent.count(userId) > 0:
                SectionContent(userId).delete()

    # ********** ---------- tests for /get/ endpoint ---------- **********
    def test_get_from_existing_entry_and_existing_section_with_valid_parameters(self):
        r = requests.get(url=GET_ENDPOINT, params = GET_REQUEST_PARAMS1)
        response = json.loads(r.text)

        assert r.status_code == 200
        assert response["section"] == GET_REQUEST_PARAMS1["section"]
        assert response["content"] == SECTION1_CONTENT1

    def test_get_from_existing_entry_and_non_existing_section_with_valid_parameters(self):
        r = requests.get(url=GET_ENDPOINT, params=GET_REQUEST_PARAMS1_NON_EXISTING_SECTION)
        response = json.loads(r.text)

        assert r.status_code == 200
        assert response["section"] == GET_REQUEST_PARAMS1_NON_EXISTING_SECTION["section"]
        assert response["content"] is None

    def test_get_from_existing_entry_with_missing_parameter(self):
        r = requests.get(url=GET_ENDPOINT, params=GET_REQUEST_MISSING_PARAMS1)

        assert r.status_code == 400
        assert not r.text

    def test_get_from_non_existing_entry(self):
        r = requests.get(url=GET_ENDPOINT, params = GET_REQUEST_PARAMS_NON_EXISTING_USER)
        response = json.loads(r.text)

        assert r.status_code == 200
        assert response["section"] == GET_REQUEST_PARAMS_NON_EXISTING_USER["section"]
        assert not response["content"]

    # ********** ---------- tests for /put/ endpoint ---------- **********
    def test_put_to_existing_entry_and_existing_section_with_valid_parameters(self):
        r = requests.put(url=PUT_ENDPOINT, data = json.dumps(PUT_REQUEST_PARAMS1))
        response = json.loads(r.text)

        assert r.status_code == 200
        assert response["section"] == PUT_REQUEST_PARAMS1["section"]
        assert response["content"] == PUT_REQUEST_PARAMS1["content"]

        r2 = requests.get(url=GET_ENDPOINT, params = PUT_REQUEST_PARAMS1)
        response2 = json.loads(r2.text)
        assert r2.status_code == 200
        assert response2["section"] == PUT_REQUEST_PARAMS1["section"]
        assert response2["content"] == PUT_REQUEST_PARAMS1["content"]

    def test_put_to_existing_entry_and_non_existing_section_with_valid_parameters(self):
        r = requests.put(url=PUT_ENDPOINT, data=json.dumps(PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION))
        response = json.loads(r.text)

        assert r.status_code == 200
        assert response["section"] == PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION["section"]
        assert response["content"] == PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION["content"]

        r2 = requests.get(url=GET_ENDPOINT, params=PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION)
        response2 = json.loads(r2.text)
        assert r2.status_code == 200
        assert response2["section"] == PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION["section"]
        assert response2["content"] == PUT_REQUEST_PARAMS1_NON_EXISTING_SECTION["content"]

    def test_put_to_non_existing_entry_with_valid_parameters(self):
        r = requests.put(url=PUT_ENDPOINT, data = json.dumps(PUT_REQUEST_PARAMS1_NON_EXISTING_USER))
        response = json.loads(r.text)

        assert r.status_code == 201
        assert response["section"] == PUT_REQUEST_PARAMS1_NON_EXISTING_USER["section"]
        assert response["content"] == PUT_REQUEST_PARAMS1_NON_EXISTING_USER["content"]

        r2 = requests.get(url=GET_ENDPOINT, params=PUT_REQUEST_PARAMS1_NON_EXISTING_USER)
        response2 = json.loads(r2.text)
        assert r2.status_code == 200
        assert response2["section"] == PUT_REQUEST_PARAMS1_NON_EXISTING_USER["section"]
        assert response2["content"] == PUT_REQUEST_PARAMS1_NON_EXISTING_USER["content"]

    def test_put_to_existing_entry_with_missing_parameter(self):
        r = requests.get(url=GET_ENDPOINT, data = json.dumps(PUT_REQUEST_MISSING_PARAMS1))

        assert r.status_code == 400
        assert not r.text


if __name__ == '__main__':
    unittest.main()
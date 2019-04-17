ASSERTION_MESSAGES = {
    'STATUS_CODE': "expected response code %i but got %i.",
    'OBJECT_EXISTS': 'expected %i existing object but there are %i.',
    'OBJECT_IN_RESPONSE': 'expected object with id %i missing in response.',
    'RESPONSE_LENGTH': 'expected %i objects in response, but it contains %i.',
    'FIELD_VALUE_EQUALS': 'expected object field %s to be equals to %s, but got %s.',
}

def assert_field_equality(resource, field_name, expected_value):
    assert resource.__dict__[field_name] == expected_value, \
        ASSERTION_MESSAGES['FIELD_VALUE_EQUALS'] % \
        (field_name, expected_value, resource.__dict__[field_name])


def assert_status_code(response, expected_code):
    """
    asserts request object has an expected status code.
    """
    assert response.status_code == expected_code, ASSERTION_MESSAGES['STATUS_CODE'] % (expected_code, response.status_code)


def assert_object_exists(cls, count=1):
    """
    asserts an object exists in the database.
    """
    total_count = cls.objects.count()
    assert total_count == count, ASSERTION_MESSAGES['OBJECT_EXISTS'] %  (count, total_count)


def assert_object_created(cls, response):
    """
    asserts an object was created in the database.
    """
    assert_status_code(response, 201 )
    assert_object_exists(cls)


def assert_response_contains_object(obj, response, is_array=True, max_count=1, status_code=200):
    """
    asserts a response object contains an existing object.
    """
    json_data = response.json()
    assert_status_code(response, status_code)

    if is_array:
        assert len(json_data) == max_count, ASSERTION_MESSAGES['RESPONSE_LENGTH'] % (max_count, len(json_data))
        json_data = json_data[0]

    assert obj.id == json_data['id'], ASSERTION_MESSAGES['OBJECT_IN_RESPONSE'] % obj.id


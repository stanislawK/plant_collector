import pytest
from marshmallow import ValidationError

from api.serializers.plant import plant_schema
from api.serializers.description import desc_schema


def test_plant_serializer_with_valida_data(new_plant):
    """
    GIVEN valid plant data and marshmallow serializer
    WHEN loading plant data
    THEN check if output is correct
    """
    result = plant_schema.load(new_plant)
    assert result["name"] == "Monstera"
    assert result["latin"] == "Monstera Adans."
    assert result["difficulty"] == 5


def test_plant_serializer_without_name(new_plant):
    """
    GIVEN plant data without name and marshmallow serializer
    WHEN loading invalid plant data
    THEN check if proper error was raised
    """
    del new_plant["name"]
    try:
        result = plant_schema.load(new_plant)
    except ValidationError as err:
        assert err.messages["name"][0] == 'Missing data for required field.'


def test_plant_serializer_with_invalid_difficulty(new_plant):
    """
    GIVEN plant data with difficuty out of range and marshmallow serializer
    WHEN loading invalid plant data
    THEN check if proper error was raised
    """
    new_plant["difficulty"] = 11
    try:
        result = plant_schema.load(new_plant)
    except ValidationError as err:
        assert err.messages["difficulty"][0] == 'Must be between 0 and 10.'


def test_desc_serializer_with_valida_data(new_desc):
    """
    GIVEN valid description data and marshmallow serializer
    WHEN loading description data
    THEN check if output is correct
    """
    result = desc_schema.load(new_desc)
    assert result["content"] == "Description content"
    assert result["source"] == "wikipedia"


def test_desc_serializer_with_invalida_data(new_desc):
    """
    GIVEN description data without content and marshmallow serializer
    WHEN loading invalid description data
    THEN check if proper error was raised
    """
    del new_desc["content"]
    try:
        result = desc_schema.load(new_desc)
    except ValidationError as err:
        assert err.messages['content'][0] == "Missing data for required field."

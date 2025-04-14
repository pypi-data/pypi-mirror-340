from citymappingworld.core import get_city_options

def test_get_city_options():
    options = get_city_options()
    assert isinstance(options, list)
    assert "label" in options[0]

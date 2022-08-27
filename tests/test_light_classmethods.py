""" Test Light classmethods
"""

from typing import List

import pytest

from busylight.lights import LightUnsupported

from . import (
    ABSTRACT_LIGHT_SUBCLASSES,
    ALL_LIGHT_SUBCLASSES,
    CONCRETE_LIGHT_SUBCLASSES,
    BOGUS_DEVICE_ID,
)


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_subclasses(subclass) -> None:
    """Call the `subclasses` class method for all Light subclasses."""

    result = subclass.subclasses()

    assert isinstance(result, list)

    for item in result:
        assert issubclass(item, subclass)


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_supported_lights(subclass) -> None:
    """Call the `supported_lights` class method for all Light subclasses."""

    result = subclass.supported_lights()

    assert isinstance(result, dict)

    for key, values in result.items():
        assert isinstance(key, str)
        for value in values:
            assert isinstance(value, str)


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_available_lights(subclass) -> None:
    """Call the `available_lights` class method for all Light subclasses."""
    result = subclass.available_lights()

    assert isinstance(result, list)

    for item in result:
        assert isinstance(item, dict)
        for key, value in item.items():
            assert isinstance(key, str)
            assert isinstance(value, (bytes, int, str, tuple))


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_supported_device_ids(subclass) -> None:
    """Call the `supported_device_ids` static method for each concrete Light subclass."""

    result = subclass.supported_device_ids()

    assert isinstance(result, dict)

    for key, value in result.items():
        assert isinstance(key, tuple)
        assert isinstance(value, str)


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_udev_rules(subclass) -> None:
    """Call the `udev_rules` class method for all Light subclasses."""
    mode = 0o0754
    result = subclass.udev_rules(mode=mode)

    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, str)
        if "MODE=" in item:
            assert f"{mode:04o}" in item


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_vendor(subclass) -> None:
    """Call the `vendor` static method for all concrete Light subclasses."""

    result = subclass.vendor()

    assert isinstance(result, str)


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_claims_known_good_lights(subclass) -> None:
    """Call the `claims` class methdo for all concrete Light subclasses
    with known good light_info dictionaries.
    """

    light_info = {}
    for key, value in subclass.supported_device_ids().items():
        light_info["device_id"] = key
        light_info["product_string"] = value

    claimed = subclass.claims(light_info)

    assert claimed


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_claims_known_bad_lights(subclass) -> None:
    """Call the `claims` class method for all concrete Light subclasses
    with known bad light_info dictionaries.
    """

    light_info = {"device_id": BOGUS_DEVICE_ID, "product_id": "nonexistent light"}

    claimed = subclass.claims(light_info)

    assert not claimed


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_all_lights(subclass) -> None:
    """Call the `all_lights` class method for all Light subclasses."""

    result = subclass.all_lights(reset=False, exclusive=False)

    assert isinstance(result, list)

    for item in result:
        assert issubclass(type(item), subclass)


@pytest.mark.parametrize("subclass", ALL_LIGHT_SUBCLASSES)
def test_light_subclass_first_light(subclass) -> None:
    """Call the `first_light` class method for all Light subclasses."""

    result = subclass.first_light(reset=False, exclusive=False)

    assert isinstance(result, subclass)


@pytest.mark.parametrize("subclass", ABSTRACT_LIGHT_SUBCLASSES)
def test_light_subclass_is_abstract(subclass) -> None:
    """Check that abstract Light subclasses self-identify correctly."""

    is_abstract = subclass._is_abstract()
    is_concrete = subclass._is_concrete()

    assert is_abstract and not is_concrete


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_is_concrete(subclass) -> None:
    """Check that concrete Light subclasses self-identify correctly."""

    is_abstract = subclass._is_abstract()
    is_concrete = subclass._is_concrete()

    assert is_concrete and not is_abstract


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_init_known_good_lights(subclass) -> None:
    """Initialize a Light subclass with known good light_info dictionaries."""

    light_info = {
        # EJO Easier to pre-populate this dictionary with these values
        #     for Agile Innovative BlinkStick than to discover
        #     them. All other concrete lights will ignore them.
        "serial_number": "BS032974-3.0",
        "release_number": 0x0200,
    }

    for key, value in subclass.supported_device_ids().items():
        light_info["device_id"] = key
        light_info["product_string"] = value
        light = subclass(light_info, reset=False, exclusive=False)
        assert isinstance(light, subclass)


@pytest.mark.parametrize("subclass", CONCRETE_LIGHT_SUBCLASSES)
def test_light_subclass_init_known_bad_lights(subclass) -> None:
    """Initialize a Light subclass with known bad light_info dictionaries."""

    light_info = {
        "serial_number": "bogus serial number",
        "release_number": 0x0,
        "device_id": BOGUS_DEVICE_ID,
        "product_string": "nonexistent light",
    }

    with pytest.raises(LightUnsupported):
        light = subclass(light_info, reset=False, exclusive=False)

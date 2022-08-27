"""
"""

import pytest

from busylight.effects import Spectrum


@pytest.mark.parametrize(
    "duty_cycle,scale,steps,frequency,phase,center,width",
    [
        (0.5, 1, 64, None, None, 128, 127),
    ],
)
def test_spectrum_init(
    duty_cycle, scale, steps, frequency, phase, center, width
) -> None:

    instance = Spectrum(duty_cycle, scale, steps, frequency, phase, center, width)

    assert instance.name == "Spectrum"

    repr_result = repr(instance)
    str_result = str(instance)

    assert isinstance(instance, Spectrum)
    assert instance.duty_cycle == duty_cycle
    assert instance.name in repr_result
    assert instance.name in str_result
    assert len(instance.colors) != 0

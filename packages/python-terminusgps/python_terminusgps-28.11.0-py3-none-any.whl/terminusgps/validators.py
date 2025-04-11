import string

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_vin_number(value: str) -> None:
    """Raises :py:exec:`ValidationError` if the value is an invalid VIN number."""
    if not len(value) == 17:
        raise ValidationError(
            _("Whoops! VIN # must be exactly 17 characters long, got %(len)s."),
            code="invalid",
            params={"len": len(value)},
        )


def validate_wialon_password(value: str) -> None:
    """Raises :py:exec:`ValidationError` if the value represents an invalid Wialon password."""
    special_symbols_0: list[str] = ["!", "@", "#", "$", "%", "^", "*"]
    special_symbols_1: list[str] = ["(", ")", "[", "]", "-", "_", "+"]
    forbidden_symbols: list[str] = [",", ":", "&", "<", ">", "'"]
    value = value.strip() if value.startswith(" ") or value.endswith(" ") else value

    if len(value) < 4:
        raise ValidationError(
            _("Password cannot be less than 4 characters in length. Got '%(len)s'."),
            code="invalid",
            params={"len": len(value)},
        )
    if len(value) > 64:
        raise ValidationError(
            _(
                "Password cannot be greater than 64 characters in length. Got '%(len)s'."
            ),
            code="invalid",
            params={"len": len(value)},
        )
    if not any([char for char in value if char in string.ascii_uppercase]):
        raise ValidationError(
            _("Password must contain at least one uppercase letter."), code="invalid"
        )
    if not any([char for char in value if char in string.ascii_lowercase]):
        raise ValidationError(
            _("Password must contain at least one lowercase letter."), code="invalid"
        )
    if not any(
        [char for char in value if char in special_symbols_0 + special_symbols_1]
    ):
        raise ValidationError(
            _("Password must contain at least one special symbol."), code="invalid"
        )
    for char in value:
        if char in forbidden_symbols:
            raise ValidationError(
                _("Password cannot contain forbidden character '%(char)s'."),
                code="invalid",
                params={"char": char},
            )

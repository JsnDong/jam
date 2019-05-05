from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

validator_cardnumber = [
    RegexValidator(r'^[0-9]{16}$', "Use format XX XXXX XXXX"),
    RegexValidator(r'^[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}$', "Use format XXXX XXX XXX")
]

def regex_validators(value):
    err = None
    for validator in validator_cardnumber:
        try:
            validator(value)
            # Valid value, return it
            return value
        except ValidationError as exc:
            err = exc
    # Value match nothing, raise error
    raise err
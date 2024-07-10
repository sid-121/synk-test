import enum
import decimal
from datetime import datetime, date
from sqlalchemy.engine.result import RowProxy
from tenant_models.exceptions import ValidationError
from phonenumbers import NumberParseException, is_valid_number, parse
import pytz

avoid_list = [
    "author_id",
    "category_id",
    "state_id",
    "facility_id",
    "owner_id",
    "presentation_id",
]


def get_result_data(
    data: RowProxy, include_id: bool = False, check_avoid_list: bool = False
) -> dict:
    result_data = {}
    for key, value in data.items():
        if isinstance(value, enum.Enum):
            result_data.update({key: value.name})
        elif isinstance(value, datetime):
            result_data.update({key: str(value)})
        elif isinstance(value, date):
            result_data.update({key: str(value)})
        elif isinstance(value, decimal.Decimal):
            result_data.update({key: float(value)})
        elif key == "id" and not include_id:
            pass
        elif key in avoid_list and check_avoid_list:
            pass
        else:
            result_data.update({key: value})

    return result_data


def get_list_result_data(
    data_list: list,
    include_id: bool = False,
    check_avoid_list: bool = False,
    use_enum_name: bool = False,
) -> dict:
    result_data = {}
    if isinstance(data_list, list):
        for data in data_list:
            for key, value in data.items():
                if isinstance(value, enum.Enum):
                    if use_enum_name:
                        result_data.update({key: value.name})
                    else:
                        result_data.update({key: value.value})
                elif isinstance(value, datetime):
                    result_data.update({key: str(value)})
                elif isinstance(value, date):
                    result_data.update({key: str(value)})
                elif isinstance(value, decimal.Decimal):
                    result_data.update({key: float(value)})
                elif key == "id" and not include_id:
                    pass
                elif key in avoid_list and check_avoid_list:
                    pass
                else:
                    result_data.update({key: value})

    return result_data


def get_list_of_dict_result_data(
    data_list: list,
    include_id: bool = False,
    check_avoid_list: bool = False,
    use_enum_name: bool = False,
) -> list:
    result_data = []
    if isinstance(data_list, list):
        for data in data_list:
            new_data = {}
            for key, value in data.items():
                if isinstance(value, enum.Enum):
                    if use_enum_name:
                        new_data.update({key: value.name})
                    else:
                        new_data.update({key: value.value})
                elif isinstance(value, datetime):
                    new_data.update({key: str(value)})
                elif isinstance(value, date):
                    new_data.update({key: str(value)})
                elif isinstance(value, decimal.Decimal):
                    new_data.update({key: float(value)})
                elif key == "id" and not include_id:
                    pass
                elif key in avoid_list and check_avoid_list:
                    pass
                else:
                    new_data.update({key: value})
            result_data.append(new_data)

    return result_data


def get_filter_validated_data(request_data: dict, validated_data: dict) -> dict:
    if validated_data:
        for key in list(validated_data):
            if not key in request_data:
                validated_data.pop(key)
    else:
        raise ValidationError("input data (validated_data) cannot be empty")

    if not validated_data:
        raise ValidationError("request body cannot be empty")
    return validated_data


def validate_number(phone_number: str) -> bool:
    """
    Description:
        This method used to verify the number is valid or not using the library phonenumbers
    Exception:
        Raise ValueError when the number is not valid
    Returns (Bool):
        Returns True if the number is valid, else False
    """
    if (
        not (len(phone_number) <= 13 and len(phone_number) >= 10)
        or phone_number[0] == "1"
    ):
        return False

    if not phone_number.startswith("+"):
        phone_number = "+1" + phone_number
    try:
        x = parse(phone_number, None)
    except NumberParseException:
        return False
    return is_valid_number(x)


def datetime_to_utc(data: dict, keys: list) -> dict:
    """
    Returns dict with timestamp converted to UTC format.
    Used to convert datetime in validated request body to UTC before inserting to db.

    Args:
        data (dict): dict with timestamp in it
        keys (list): list of keys whose values are of type timestamp

    Returns:
        dict: dict with the modified data
    """
    try:
        for key in keys:
            if isinstance(data.get(key, None), datetime):
                data[key] = datetime.utcfromtimestamp(data.get(key).timestamp())
    except AttributeError:
        pass
    return data


def utc_to_isoformat(data: dict, keys: list) -> dict:
    """
    Returns data with +00:00 appended to the value of the key.
    Used to format UTC strings from the db before inserting it in response body.

    Args:
        data (dict): data with timestamp in it
        keys (list): list of keys whose values are strings in iso format
    """
    try:
        for key in keys:
            if data.get(key, None):
                data[key] = (
                    datetime.fromisoformat(data.get(key, None))
                    .replace(microsecond=0)
                    .astimezone()
                    .replace(tzinfo=pytz.utc)
                    .isoformat()
                )
    except AttributeError:
        pass
    return data

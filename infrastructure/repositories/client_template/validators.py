import logging
from typing import Sequence

from pydantic import ValidationError

logger = logging.getLogger(__name__)


def validate_dict(response: dict, base_model):
    """Валидация dict.

    :param response:
    :param base_model:
    :return:
    :raise: ValidationError
    """
    try:
        return base_model(**response)
    except TypeError as err:
        logger.error(f"TypeError объекта response {response}\n{err}")
        raise err
    except ValidationError as err:
        logger.error(f"ValidationError объекта response {response}\n{err}")
        raise err


def validate_list(response: Sequence[dict], base_model) -> list:
    """Валидация list.

    :param response:
    :param base_model:
    :return: list
    :raise: ValidationError
    """
    return [validate_dict(item, base_model) for item in response]

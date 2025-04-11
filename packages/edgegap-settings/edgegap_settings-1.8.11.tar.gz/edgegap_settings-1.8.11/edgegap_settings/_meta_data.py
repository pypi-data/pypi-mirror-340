from typing import Annotated

from pydantic_settings import BaseSettings

from ._factory import SettingsFactory

_ATTRIBUTE_NAME = 'marked_for_checkup'


def add_to_checkup_list(class_def):
    """
    Add metadata to the class that will be detected by the `check_settings` function.
    """
    if not issubclass(class_def, BaseSettings):
        raise ValueError('Only subclasses of BaseSettings can be added to the checkup list.')
    class_def = Annotated[class_def, _ATTRIBUTE_NAME]

    return class_def


def _all_defined_subclasses(cls):
    """
    Recursively get all subclasses of a class.
    """
    return set(cls.__subclasses__()).union(s for c in cls.__subclasses__() for s in _all_defined_subclasses(c))


def check_settings():
    """
    Retrieve all classes that are marked for checkup and call SettingsFactory.from_settings on them.
    """
    to_check_classes = (
        c
        for c in _all_defined_subclasses(BaseSettings)
        if hasattr(c, '__metadata__') and _ATTRIBUTE_NAME in c.__metadata__
    )

    for to_check_class in to_check_classes:
        SettingsFactory.from_settings(to_check_class)

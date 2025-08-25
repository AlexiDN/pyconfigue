from typing import Any, get_type_hints

from pydantic import BaseModel

from pyconfigue.utils.utils import is_optional


class ConFigueModel:
    """Base Configuration Model
    Use this as a parent class to define your
     configuration Model
    """


class ValidatorModel(BaseModel):
    """Base Configuration Model Validator class."""

    @classmethod
    def model_validate(
        cls,
        obj: dict[str, Any],
        *args: tuple[Any],
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
        ignore_missing_fields: bool = False,
    ) -> "ValidatorModel":
        """Validate the data using the model and return an instance of the Model"""
        if not obj and args:
            obj = args[0]
        if ignore_missing_fields:
            # Get type hints with resolved forward refs
            hints = get_type_hints(cls, include_extras=True)
            # Only fill in None for fields that explicitly allow None
            for field, type_ in hints.items():
                if field not in obj and is_optional(type_):
                    obj[field] = None

        return super().model_validate(
            obj,
            strict=strict,
            from_attributes=from_attributes,
            context=context,
            by_alias=by_alias,
            by_name=by_name,
        )

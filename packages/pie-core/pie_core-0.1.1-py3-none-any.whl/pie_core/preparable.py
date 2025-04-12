import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PreparableMixin:
    # list of attribute names that need to be set by _prepare()
    PREPARED_ATTRIBUTES: List[str] = []

    @property
    def is_prepared(self) -> bool:
        """Returns True, iff all attributes listed in PREPARED_ATTRIBUTES are set.

        Note: Attributes set to None are not considered to be prepared!
        """
        return all(
            getattr(self, attribute, None) is not None for attribute in self.PREPARED_ATTRIBUTES
        )

    @property
    def prepared_attributes(self) -> Dict[str, Any]:
        if not self.is_prepared:
            raise Exception("The module is not prepared.")
        return {param: getattr(self, param) for param in self.PREPARED_ATTRIBUTES}

    def _prepare(self, *args, **kwargs) -> None:
        """This method needs to set all attributes listed in PREPARED_ATTRIBUTES."""
        pass

    def _post_prepare(self) -> None:
        """Any code to do further one-time setup, but that requires the prepared attributes."""
        pass

    def assert_is_prepared(self, msg: Optional[str] = None) -> None:
        if not self.is_prepared:
            attributes_not_prepared = [
                param for param in self.PREPARED_ATTRIBUTES if getattr(self, param, None) is None
            ]
            raise Exception(
                f"{msg or ''} Required attributes that are not set: {str(attributes_not_prepared)}"
            )

    def post_prepare(self) -> None:
        self.assert_is_prepared()
        self._post_prepare()

    def prepare(self, *args, **kwargs) -> None:
        if self.is_prepared:
            if len(self.PREPARED_ATTRIBUTES) > 0:
                msg = f"The {self.__class__.__name__} is already prepared, do not prepare again."
                for k, v in self.prepared_attributes.items():
                    msg += f"\n{k} = {str(v)}"
                logger.warning(msg)
        else:
            self._prepare(*args, **kwargs)
            self.assert_is_prepared(
                msg=f"_prepare() was called, but the {self.__class__.__name__} is not prepared."
            )
        self._post_prepare()
        return None

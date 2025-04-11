from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Union,
    overload,
)
from typing_extensions import Self

from instaui.vars import Ref
from instaui.components.value_element import ValueElement
from instaui.components.element import Element
from instaui.vars.types import TMaybeRef
from instaui.components.vfor import VFor

if TYPE_CHECKING:
    import instaui.vars as ui_vars


_T_Select_Value = Union[List[str], str]


class Select(ValueElement[Union[List[str], str]]):
    def __init__(
        self,
        value: Union[_T_Select_Value, ui_vars.TMaybeRef[_T_Select_Value], None] = None,
        *,
        model_value: Union[str, ui_vars.TMaybeRef[str], None] = None,
    ):
        super().__init__("select", value, is_html_component=True)

        if model_value is not None:
            self.props({"value": model_value})

    @overload
    def on_change(self, handler: Callable, *, key: Optional[str] = None) -> Self: ...

    @overload
    def on_change(
        self,
        handler: str,
        *,
        bindings: Optional[Dict] = None,
        key: Optional[str] = None,
    ) -> Self: ...

    def on_change(
        self,
        handler: Union[Callable, str],
        *,
        bindings: Optional[Dict] = None,
        key: Optional[str] = None,
    ):
        self.on("change", handler, bindings=bindings, key=key)  # type: ignore
        return self

    @classmethod
    def from_list(
        cls,
        options: TMaybeRef[List],
        value: Union[_T_Select_Value, ui_vars.TMaybeRef[_T_Select_Value], None] = None,
    ) -> Select:
        with cls(value) as select:
            with VFor(options) as item:
                Select.Option(item)  # type: ignore

        return select

    class Option(Element):
        def __init__(
            self,
            text: Optional[ui_vars.TMaybeRef[str]] = None,
            value: Optional[ui_vars.TMaybeRef[str]] = None,
            disabled: Optional[ui_vars.TMaybeRef[bool]] = None,
        ):
            props = {
                key: value
                for key, value in {
                    "text": text,
                    "value": value,
                    "disabled": disabled,
                }.items()
                if value is not None
            }
            super().__init__("option")

            self._props.update(props)

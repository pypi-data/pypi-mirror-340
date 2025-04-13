"""Field handlers for numeric types."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import reflex as rx

from reflexions.model_form.utils import get_default_value, get_json_schema_extra

from .base import FieldHandler, FieldHandlerRegistry


if TYPE_CHECKING:
    from collections.abc import Callable

    import pydantic


class IntHandler(FieldHandler):
    """Handler for integer fields."""

    def supports(
        self, type_annotation: Any, field_info: pydantic.fields.FieldInfo | None = None
    ) -> bool:
        """Check if this handler supports the field (int only)."""
        return type_annotation is int

    def create_widget(
        self,
        field_name: str,
        field_info: pydantic.fields.FieldInfo,
        value: Any,
        on_change: Callable[[Any], None],
        error: str | None = None,
    ) -> rx.Component:
        """Create a widget for integer fields.

        Args:
            field_name: Name of the field
            field_info: Pydantic field info
            value: Current value
            on_change: Callback for value changes
            error: Optional error message

        Returns:
            Form input component for integers
        """
        # Get constraints from field_info
        gt = getattr(field_info, "gt", None)
        ge = getattr(field_info, "ge", None)
        lt = getattr(field_info, "lt", None)
        le = getattr(field_info, "le", None)

        # Determine min/max values based on constraints
        min_value = ge if ge is not None else (gt + 1 if gt is not None else None)
        max_value = le if le is not None else (lt - 1 if lt is not None else None)

        # Field label
        label = field_info.title or field_name.replace("_", " ").capitalize()
        extras = get_json_schema_extra(field_info)
        step = extras.get("step", 1)
        return rx.vstack(
            rx.hstack(
                rx.text(label, as_="label", for_=field_name),
                rx.badge("Required", color_scheme="red", variant="soft", size="1")
                if field_info.is_required()
                else None,
                align_items="center",
            ),
            rx.input(
                type="number",
                id=field_name,
                value=value,
                placeholder=field_info.description,
                on_change=on_change,
                step=step,
                min=min_value,
                max=max_value,
                border_color=rx.cond(error is not None, "red.500", None),
            ),
            rx.text(error, color="red.500", font_size="sm") if error else None,
            rx.text(
                field_info.description,
                color="gray.500",
                font_size="sm",
            )
            if field_info.description
            else None,
            align_items="start",
            width="100%",
            spacing="1",
        )

    def get_default_value(self, field_info: pydantic.fields.FieldInfo) -> Any:
        """Get default value for an integer field.

        Args:
            field_info: Pydantic field info

        Returns:
            Default value for the field
        """
        return get_default_value(field_info, 0)


# Register the handler
registry = FieldHandlerRegistry()
registry.register(IntHandler())

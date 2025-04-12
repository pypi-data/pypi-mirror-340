from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any

from jinja2.utils import pass_context
from markupsafe import Markup

from mkdocstrings_handlers.graphql._internal.enumerations import Kind

if TYPE_CHECKING:
    from jinja2.runtime import Context

    from mkdocstrings_handlers.graphql._internal.models import Node, OperationTypeNode


@pass_context
def format_signature(
    context: Context,
    callable_path: Markup,
    operation: OperationTypeNode,
    *,
    annotations: bool | None = None,
) -> str:
    """Formats a signature.

    Args:
        context: Jinja context, passed automatically.
        callable_path: The path of the callable we render the signature of.
        operation: The operation we render the signature of.
        annotations: Whether to show type annotation.

    Returns:
        The same code, formatted.
    """
    env = context.environment
    template = env.get_template("signature.html.jinja")

    if annotations is None:
        new_context = context.parent
    else:
        new_context = dict(context.parent)
        new_context["config"] = replace(new_context["config"], show_signature_annotations=annotations)

    signature = template.render(new_context, operation=operation, signature=True)
    signature = _format_signature(callable_path, signature)
    highlight_kwargs: dict[str, Any] = {
        "src": Markup.escape(signature),
        "language": "graphql",
        "inline": False,
        "linenums": False,
        "classes": ["doc-signature"],
    }
    return str(env.filters["highlight"](**highlight_kwargs))  # pyright:ignore[reportCallIssue]


def get_template(node: Node) -> str:
    """Returns the template name used to render a node.

    Args:
        node: A node.

    Returns:
        A template name.
    """
    return f"{map_kind(node.kind)}.html.jinja"


def map_kind(kind: Kind) -> str:
    """Maps ``kind`` to its string value."""
    if kind in {Kind.INPUT, Kind.INTERFACE}:
        return Kind.OBJECT.value
    return kind.value


def _format_signature(name: Markup, signature: str) -> str:
    name_str = str(name).strip()
    signature = signature.strip()
    return name_str + signature

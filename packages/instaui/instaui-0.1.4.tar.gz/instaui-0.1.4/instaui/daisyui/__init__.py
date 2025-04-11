"""
Easy to use DaisyUI components for InstaUI.

Example usage:
.. code-block:: python
    from instaui import ui, daisyui as dsui

    dsui.use()

    @ui.page("/")
    def index_page():
        dsui.checkbox(checked=True)
"""

__all__ = ["use", "checkbox", "button"]


from .checkbox import Checkbox as checkbox
from .button import Button as button
from ._index import use_daisyui as use

from pathlib import Path
from typing import ClassVar, Iterable, List, Union
from warnings import warn
from instaui import ui
from instaui.runtime import get_app_slot

_STATIC_DIR = Path(__file__).parent / "static"
_STYLES_DIR = _STATIC_DIR / "styles"
_LANGUAGE_DIR = _STATIC_DIR / "languages"
_CORE_JS_FILE = _STATIC_DIR / "core.min.js"

_LANGUAGE_IMPORT_NAME = "highlight.js/languages/"
_CORE_JS_IMPORT_NAME_ZERO_MODE = "highlight.js/lib/core.min.js"

_IMPORT_MAPS = {
    "highlight.js/lib/": _STATIC_DIR,
    _LANGUAGE_IMPORT_NAME: _LANGUAGE_DIR,
}


class Code(
    ui.element,
    esm="./code.js",
    externals=_IMPORT_MAPS,
    css=[_STYLES_DIR],
):
    _language_folder: ClassVar[Path] = _LANGUAGE_DIR

    def __init__(
        self,
        code: ui.TMaybeRef[str],
        *,
        language: ui.TMaybeRef[str] = "python",
        theme: str = "default",
    ):
        super().__init__()
        self.props({"code": code})

        mode = get_app_slot().mode

        if language:
            self.props({"language": language})

            if mode == "zero":
                _try_update_dependencies_by_zero(self, language)

        self.update_dependencies(css=[_STYLES_DIR / f"{theme}.min.css"])

    @classmethod
    def reset_language_folder(cls, folder: Path):
        """Reset the language folder for all js files.

        Args:
            folder (Path): The new language folder.

        Examples
        .. code-block:: python
            from instaui import ui

            # must be called outside of page function
            ui.code.reset_language_folder(Path("my_lang_folder"))
        """
        assert cls.dependency
        cls.dependency.externals.update({_LANGUAGE_IMPORT_NAME: folder})
        cls._language_folder = folder

    @classmethod
    def specified_language_by_zero_mode(
        cls, folder_or_files: Union[Path, Iterable[Path]]
    ):
        """Specify the language files for zero mode.

        Args:
            folder_or_files (Union[Path, Iterable[Path]]): The folder or files to be imported.

        Examples
        .. code-block:: python
            from instaui import ui,zero

            def page():
                ...

            with zero() as z:
                ui.code.specified_language_by_zero_mode(Path("my_lang_folder"))
                page()
        """
        if not isinstance(folder_or_files, Iterable):
            is_dir = folder_or_files.is_dir()
            files = (
                list(folder_or_files.glob("*.min.js")) if is_dir else [folder_or_files]
            )

        else:
            files = folder_or_files

        externals = {}
        for file in files:
            language = file.stem
            externals[f"{_LANGUAGE_IMPORT_NAME}{language}.min.js"] = file

        cls.dependency.externals.update(externals)  # type: ignore


def _try_update_dependencies_by_zero(code: Code, language: ui.TMaybeRef[str]):
    if isinstance(language, str):
        code.update_dependencies(
            externals={
                f"{_LANGUAGE_IMPORT_NAME}{language}.min.js": code._language_folder
                / f"{language}.min.js",
                _CORE_JS_IMPORT_NAME_ZERO_MODE: _CORE_JS_FILE,
            }
        )
    else:
        warn(
            "language must be a string in zero mode , or you can call specified_language_by_zero_mode() to specify the language files",
            stacklevel=2,
        )

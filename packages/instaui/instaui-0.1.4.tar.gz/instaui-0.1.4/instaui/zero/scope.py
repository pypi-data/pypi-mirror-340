from pathlib import Path
from typing import Union
from instaui.runtime import new_app_slot, reset_app_slot
from contextlib import contextmanager
from .func import to_html, to_html_str, get_template_model
from instaui.template.zero_template import ZeroTemplateModel


@contextmanager
def scope():
    token = new_app_slot("zero")
    yield Wrapper()
    reset_app_slot(token)


class Wrapper:
    def to_html(self, file: Union[str, Path]):
        file = self._get_caller_path(file)
        return to_html(file)

    def to_html_str(self):
        return to_html_str()

    def to_debug_report(self, file: Union[str, Path]):
        file = self._get_caller_path(file)

        # Custom component dependencies must be recorded only during actual execution
        to_html_str()
        model = get_template_model()
        with scope() as s:
            _create_debug_report(model)
            s.to_html(file.resolve().absolute())

    @staticmethod
    def _get_caller_path(file: Union[str, Path]) -> Path:
        if isinstance(file, str):
            import inspect

            frame = inspect.currentframe().f_back.f_back  # type: ignore
            assert frame is not None
            script_file = inspect.getfile(frame)
            file = Path(script_file).parent.joinpath(file)

        return file


def _create_debug_report(model: ZeroTemplateModel):
    from instaui import ui, html

    no_exists_path_class = "ex-no-exists-path"

    def _path_exists_class(path: Path):
        return "" if path.exists() else no_exists_path_class

    ui.use_tailwind()
    ui.add_style(rf".{no_exists_path_class} {{background-color: red;color: white;}}")

    with ui.column().classes("gap-2"):
        # import maps
        html.paragraph("import maps")
        with ui.grid(columns="auto 1fr").classes(
            "gap-4 border-2 border-gray-200 p-4 place-center"
        ):
            html.span("name")
            html.span("path")

            html.span("vue")
            html.span(str(model.vue_js_code))

            html.span("instaui")
            html.span(str(model.instaui_js_code))

            for name, url in model.extra_import_maps.items():
                if isinstance(url, Path) and url.is_file():
                    html.span(name)
                    html.span(str(url.resolve().absolute())).classes(
                        _path_exists_class(url)
                    )

        # css links
        html.paragraph("css links")
        with ui.column().classes("gap-4 border-2 border-gray-200 p-4 place-center"):
            for link in model.css_links:
                if isinstance(link, Path) and link.is_file():
                    html.span(str(link)).classes(_path_exists_class(link))

        # js links
        html.paragraph("js links")
        with ui.column().classes("gap-4 border-2 border-gray-200 p-4 place-center"):
            for info in model.js_links:
                if isinstance(info.link, Path) and info.link.is_file():
                    html.span(str(info.link)).classes(_path_exists_class(info.link))

        # custom components
        html.paragraph("custom components")
        with ui.grid(columns="auto 1fr").classes(
            "gap-4 border-2 border-gray-200 p-4 place-center"
        ):
            html.span("name")
            html.span("js file path")

            for info in model.vue_app_component:
                html.span(info.name)

                if isinstance(info.url, Path) and info.url.is_file():
                    html.span(str(info.url)).classes(_path_exists_class(info.url))
                else:
                    html.span("not file")

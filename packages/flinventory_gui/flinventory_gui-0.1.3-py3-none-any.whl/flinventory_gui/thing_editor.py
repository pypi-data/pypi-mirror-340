"""Functions and classes for a display that allows changing the information about a thing."""

import asyncio
import os
import urllib.request
from typing import (
    Union,
    Callable,
    Any,
    Literal,
    Optional,
    override,
    cast,
    Iterable,
    MutableMapping,
)
from urllib.error import ContentTooShortError

import nicegui
from nicegui import ui

import flinventory
from flinventory import BoxedThing


def try_conversion(
    value: str, conversions: Iterable[Union[Callable[[str], Any], Literal["bool"]]]
) -> Any:
    """Try to convert value into other values.

    Args:
        value: value to be converted
        conversions: tuple of conversion functions that raise Exception upon failure
            or "bool" which converts the strings "true", "false"
    """
    for conversion in conversions:
        if conversion == "bool":
            if value.lower() == "true":
                return True
            if value.upper() == "false":
                return False
            continue
        try:
            return conversion(value)
        except Exception:  # pylint: disable=broad-exception-caught
            pass
    return value


class SlowInputSaver[Container: MutableMapping]:
    """Saves content of an input field to a dict-like (a BoxedThing).

    Does so with a bit of delay to avoid creating save operations if
    new letters are typed immediately after.

    Can be used as an on-change-action connected to an input field.

    Maybe it makes sense to make SlowInputSaver dependent on the type of the data
    object. We will see.
    """

    def __init__(
        self,
        data: Container,
        member: flinventory.defaulted_data.Key,
    ):
        """Create a SlowInputSaver.

        Args:
            data: the data object (think thing) to be altered
            member: which information to be altered. thing[member] = <something suitable>
                must be allowed
        """
        self.data = data
        self.member = member
        self._running_queries: list[asyncio.Task] = []

    def converter(self, value: Any) -> Any:
        """A hook for subclasses to override for value conversion.

        Since subclasses might do different things with it, it needs to stay a method.
        The linter gets it by actually overriding it in another class. (Where it still
        could be a static method.)
        """
        return value

    def setter(self, value: Any):
        """How the value of the input element is saved.

        This can be overridden by subclasses.
        """
        if not value:
            try:
                del self.data[self.member]
            except KeyError:
                # already gone, so already fine
                pass
        else:
            self.data[self.member] = value

    async def __call__(self, event: nicegui.events.ValueChangeEventArguments):
        """Value has changed. Now save it. If saving is not cancelled by further changes."""
        for query in self._running_queries:
            query.cancel()
        sleep = asyncio.create_task(asyncio.sleep(1))
        self._running_queries.append(sleep)
        try:
            await sleep
        except asyncio.exceptions.CancelledError:
            # the next letter was already typed, do not search and rerender for this query
            return
        self.setter(self.converter(event.value))


class SlowSignChanger(SlowInputSaver[flinventory.Sign]):
    """Special case for signs: add resetting printed attribute."""

    @override
    def setter(self, value: Any):
        """Sets the value and sets printed to false."""
        if not value:
            if "printed" in self.data and self.member in self.data:
                del self.data["printed"]
            try:
                del self.data[self.member]
            except KeyError:
                # already not there, fine
                pass
        else:
            previous = self.data.get(self.member, "")
            self.data[self.member] = try_conversion(
                value,
                (
                    cast(Callable[[str], Any], int),
                    cast(Callable[[str], Any], float),
                    "bool",
                ),
            )
            if previous != self.data[self.member]:
                try:
                    del self.data["printed"]
                except KeyError:
                    pass


class SlowListChanger(SlowInputSaver):
    """Special case for alt names: add splitting at ;"""

    @override
    def converter(self, value: Any) -> Any:
        """Split at ;."""
        return list(filter(None, map(str.strip, value.split(";"))))


def update_location_element(
    location_ui_element, loc: flinventory.Location, focus: Optional[str] = None
):
    """List location information with input fields.

    Args:
        location_ui_element: ui_element which content get replaced
        loc: location data to be displayed
        focus: the level name of the schema which input field should have the cursor
            None if no focus should be set
    """
    location_ui_element.clear()
    with location_ui_element:
        location_info = loc.to_jsonable_data()
        schema_hierarchy = loc.schema.get_schema_hierarchy(loc)
        ui.label(str(schema_hierarchy[0].name))
        for level in schema_hierarchy:
            try:
                level_name = level.levelname
            except flinventory.location.InvalidLocation:
                # bottom most location (in hierarchy) has no subs and therefore
                # needs no input
                continue
            ui.input(
                label=level.levelname,
                value=str(location_info.get(level.levelname, "")),
                autocomplete=(
                    list(map(str, subs))
                    if (subs := level.get_valid_subs()) is not None
                    else None
                ),  # is not None because of check before
            ).props(
                "autogrow dense" + (" autofocus" if level_name == focus else "")
            ).on_value_change(
                SlowLocationSaver(loc, level, location_ui_element)
            ).tooltip(
                ", ".join(map(str, subs))
                if (subs := level.get_valid_subs(shortcuts="()"))
                else "Any value is valid. Probably integers are reasonable."
            )
        additional_info = [
            (key, value)
            for key, value in location_info.items()
            if not any(key == schema.levelname for schema in schema_hierarchy)
        ]
        if additional_info:
            ui.label("Unused location information:")
        for key, value in additional_info:
            ui.label(f"{key}: {value}")


class SlowImageFetcher(SlowInputSaver[flinventory.Thing]):
    """Special case for image url.

    In addition to saving the inputted URL,
    this saver tries to fetch the specified url and saves it as an image if it is one.

    If the fetched file is huge, this might be problematic.
    Do I assume no malicious actor?
    """

    @override
    def converter(self, value: str) -> str:
        """Add http if no protocol is given."""
        if "://" not in value:
            return "http://" + value
        return value

    @override
    def setter(self, value: str):
        """Saves the URL and tries to save the linked image.

        If the url is removed, the image is not removed. Need a separate button for that.
        If an image exists, it is overwritten.
        It is assumed that there is some data backup system like a git repository.

        todo: show image after download.
        """
        super().setter(value)
        try:
            if any(
                value.lower().endswith(extension := image_type)
                for image_type in flinventory.constant.IMAGE_FILE_TYPES
            ):
                extension = "." + extension
            else:
                extension = ""
            urllib.request.urlretrieve(
                value,
                os.path.join(
                    self.data.directory,
                    flinventory.constant.IMAGE_FILE_BASE + extension,
                ),
            )
        except urllib.error.ContentTooShortError as interrupted:
            ui.notification(
                f"Error downloading image from {value}: \n"
                f"reason: {interrupted.reason}\n"
                f"aim filename: {interrupted.filename}\n"
                f"other info: {interrupted.args}, {interrupted}"
            )
        except ValueError as unknown_url:
            ui.notification(f"No download of {value} possible: {unknown_url}")
        except urllib.error.HTTPError as http_error:
            ui.notification(f"Download unsuccessful: {http_error}.")
        except FileNotFoundError as directory_missing:
            ui.notification(
                f"Saving image failed. Programming error: {directory_missing}"
            )


class SlowLocationSaver(SlowInputSaver[flinventory.Location]):
    """Special case for location info."""

    def __init__(
        self,
        data: flinventory.Location,
        level: flinventory.Schema,
        ui_element: ui.element,
    ):
        """Create a special saver that handles location data.

        Args:
            data: the location
            level: the level including the level name that is changed
            ui_element: the ui element that needs update after a change
        """
        super().__init__(data, level.levelname)
        self.level = level
        self.ui_element = ui_element

    @override
    def converter(self, value: Any) -> Any:
        """Convert to bool or int if possible."""
        return try_conversion(value, (int, "bool"))

    @override
    def setter(self, value: Any):
        """Set the value and update the ui."""
        try:
            self.level.get_subschema(value)
        except flinventory.location.InvalidLocationSchema as error:
            print("InvalidLocationSchema: ", error)
        except flinventory.location.InvalidLocation:
            print("Do not save")
        else:
            # no special handling for empty data. That is done in location code
            self.data[self.level.levelname] = value
            update_location_element(
                self.ui_element,
                loc=self.data,
                focus=self.level.levelname,
            )


def show_thing_changer(
    ui_element: nicegui.ui.element, thing: BoxedThing, options: flinventory.Options
) -> None:
    """Clear content of ui element and instead display editing fields.

    Args:
        ui_element: the ui element (e.g. a card) on which to show the thing changing ui
        thing: the thing to change
        options: options including the languages
    """
    input_fields: dict[tuple[str, str] | str, ui.element] = {}

    print(
        f"Try to let edit {thing.best('name', backup="a new thing")} with {id(ui_element)}."
    )
    ui_element.clear()
    with ui_element:
        with ui.row():
            with ui.column():
                for language in options.languages:
                    member: tuple[str, str] | str
                    for member in ("name", "description"):
                        input_fields[member, language] = (
                            ui.input(
                                label=f"{member} ({language})",
                                value=thing.thing.get_undefaulted(
                                    (member, language), backup=""
                                ),
                            )
                            .props("autogrow dense")
                            .on_value_change(
                                SlowInputSaver(thing.thing, (member, language))
                            )  # thing instead of thing.thing works as well but gives type error
                            # since thing is not officially a mapping
                        )
                    member = "name_alt"
                    input_fields[member, language] = (
                        ui.input(
                            label=f"{member} ({language}) (;-separated)",
                            value="; ".join(
                                thing.thing.get_undefaulted(
                                    (member, language), backup=[]
                                )
                            ),
                        )
                        .props("autogrow dense")
                        .on_value_change(
                            SlowListChanger(thing.thing, (member, language))
                        )
                    )
                input_fields["image_url"] = (
                    ui.input(
                        label="image url",
                        value=thing.thing.get_undefaulted("image_url", backup=""),
                    )
                    .props("dense")
                    .on_value_change(SlowImageFetcher(thing.thing, "image_url"))
                )
            with ui.column() as location_column:
                update_location_element(location_column, thing.location)
            with ui.column():
                for sign_member, lang, tooltip in (
                    ("width", "", "[cm]"),
                    # cm needs to be replaced by options.length_unit once this option is actually used
                    ("height", "", "[cm]"),
                    ("name", options.languages[0], "default: main name"),
                    ("name", options.languages[1], "default: main name"),
                    (
                        "fontsize",
                        options.languages[0],
                        f"default: {flinventory.signprinter_latex.STANDARD_FONT_SIZE_GERMAN}",
                    ),
                    (
                        "fontsize",
                        options.languages[1],
                        f"default: {flinventory.signprinter_latex.STANDARD_FONTSIZE_ENGLISH}",
                    ),
                    (
                        "location_shift_down",
                        "",
                        f"default: {flinventory.signprinter_latex.STANDARD_LOCATION_SHIFT_DOWN}",
                    ),
                ):
                    label = f"sign {sign_member} {f'({lang})' if lang else ''}"
                    member = (sign_member, lang) if lang else sign_member
                    input_fields[f"sign.{member}"] = (
                        ui.input(
                            label=label,
                            value=thing.sign.get_undefaulted(member, backup=""),
                        )
                        .props("autogrow dense")
                        .on_value_change(SlowSignChanger(thing.sign, member))
                    )
                    if tooltip:
                        input_fields[f"sign.{member}"].tooltip(tooltip)
            if image := thing.thing.image_path():
                ui.image(image).props("width=50%").props("height=100px").props(
                    "fit='scale-down'"
                )

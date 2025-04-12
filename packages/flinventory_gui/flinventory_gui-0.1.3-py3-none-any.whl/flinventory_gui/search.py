"""Search in a thing list."""

import argparse
import asyncio
import itertools
import os.path
import re
import time
from typing import Optional, Iterable, Callable, Union, Any, Literal, cast
import nicegui
from nicegui import ui

import flinventory
from flinventory import BoxedThing, inventory_io, Inventory

from . import thing_editor

STATIC_DIRECTORY = "website_resources"
"""Directory in the data directory where static files are located."""
FAVICON = "favicon.ico"
"""File name of the favicon in the STATIC_DIRECTORY."""

gl_options: argparse.Namespace
"""Global (module-wide) variables."""


def get_options() -> argparse.Namespace:
    """Abuse argparse for collecting file names."""
    parser = argparse.ArgumentParser()
    inventory_io.add_file_args(parser)
    parser.add_argument(
        "--port",
        "-p",
        help="Port on which to serve the website.",
        type=int,
        default=11111,
    )
    parser.add_argument(
        "--host",
        help="Host on which to run. "
        "For some cases 0.0.0.0 is necessary for accessability from outside. "
        "Passed to nicegui.ui.run.",
        default="0.0.0.0",
    )
    parser.add_argument(
        "--title",
        help="Title shown in the tab name in the browser.",
        default="Fahrradteile",
    )
    return parser.parse_args()




def load_data() -> Inventory:
    """Load data from text files and save to global thing list.

    Could implement that data is only loaded when necessary.
    Then an argument force would be useful to reload.

    Note that old things and other data might still be floating around.

    The only real added benefit of this function is the timing.

    Returns:
        the loaded inventory. Can be used to replace gl_inventory
    """
    start = time.monotonic()
    inventory = Inventory.from_json_files(directory=gl_options.dataDirectory)
    end = time.monotonic()
    print(f"Data loaded in {end-start} seconds.")
    ui.notify(f"Data loaded in {end-start} seconds.", position="top", type="positive")
    return inventory




def save_data() -> None:
    """Save things to files.

    This should be used sparingly because it needs to open and write hundreds of files,
    mostly unnecessary since during every change data is already written.
    """
    gl_inventory.save()
    ui.notify(message="Data saved", position="top", type="positive")


def antilen(string: str):
    """Return a bigger number for shorter strings, except 0 for ""."""
    return 1 / len(string) if string else 0


async def find_things(
    things: list[BoxedThing], search_string: str, max_number: int = 10
) -> Iterable[BoxedThing]:
    """Gives things that the user might have searched for.

    Args:
        things: the list of things to search in
        search_string: Input of user
        max_number: maximum number of returned things
    Returns:
        list of things that somehow include the search string
    """
    fuzzy = re.compile(
        ".*" + ".*".join(map(str.strip, search_string)) + ".*", flags=re.IGNORECASE
    )
    score_categories = ("startswith", "startswithLower", "inLower", "fuzzy")

    def match_score_one_string(string: Optional[str]) -> dict[str, float]:
        """Sortable tuple of decreasing importance. Compare just string to search string."""
        if string is None:
            return {category: 0 for category in score_categories}
        return {
            "startswith": antilen(string) if string.startswith(search_string) else 0,
            "startswithLower": (
                antilen(string)
                if string.lower().startswith(search_string.lower())
                else 0
            ),
            "inLower": (
                antilen(string) if search_string.lower() in string.lower() else 0
            ),
            "fuzzy": antilen(string) if bool(fuzzy.match(string)) else 0,
        }

    def max_scores(scores: Iterable[dict[str, float]]) -> dict[str, float]:
        """Use best score.

        Assume that all dicts have the same keys: score_categories

        Args:
            scores: tuple[score_category : score]
        Returns:
            category: max_score
        """
        try:
            return {
                key: max((score[key] for score in scores)) for key in score_categories
            }
        except ValueError:  # if iterable is empty
            return {category: 0 for category in score_categories}

    def match_score(thing: BoxedThing) -> tuple[float, ...]:
        """Return sortable tuple of decreasing importance.

        Good matches have high numbers.
        """
        assert isinstance(thing, BoxedThing)
        score_name = match_score_one_string(thing.best("name", backup=""))
        score_name_lang = max_scores(
            map(
                match_score_one_string,
                cast(Iterable[str], cast(dict, thing.get("name", {})).values()),
            )
        )
        score_name_alt = max_scores(
            map(
                match_score_one_string,
                itertools.chain(
                    *cast(dict[str, tuple[str]], thing.get("name_alt", {})).values()
                ),
            )
        )
        score_description = max_scores(
            map(
                match_score_one_string,
                cast(Iterable[str], cast(dict, thing.get("description", {})).values()),
            )
        )
        return (
            score_name["startswith"],
            score_name_lang["startswith"],
            score_name["startswithLower"],
            score_name_lang["startswithLower"],
            score_name_alt["startswith"],
            score_name_alt["startswithLower"],
            score_name["inLower"],
            score_name_lang["inLower"],
            score_name_alt["inLower"],
            score_name["fuzzy"],
            score_name_lang["fuzzy"],
            score_name_alt["fuzzy"],
            score_description["inLower"],
            score_description["fuzzy"],
        )

    if search_string:
        scored_things = [(thing, match_score(thing)) for thing in things]
        return map(
            lambda pair: pair[0],
            sorted(
                filter(lambda pair: any(pair[1]), scored_things),
                key=lambda pair: pair[1],
                reverse=True,
            )[:max_number],
        )
    return []


def navigation_row():
    """Add a navigation row with save and page change buttons."""
    with ui.row():
        # should use the things as they are when clicked: global variable
        ui.button("Save").on_click(lambda click_event: save_data())
        ui.button("New thing").on_click(lambda click_event: new_thing())
        ui.button("Search").on_click(lambda click_event: ui.navigate.to(search_page))


@ui.page("/editThing/{thing}")
def edit_thing(thing: Optional[str] = None):
    """A page that allows to edit a thing and possibly create it.

    Args:
        thing: the id of the thing (its directory name)
          if empty or None or 'new' or 'neu', create a new thing
    """
    print("thing_definer called")
    navigation_row()
    if thing in (None, "", "new", "neu"):
        thing = gl_inventory.get_id(gl_inventory.add_thing())
        print(f"Create new thing {thing}")
        ui.navigate.to(f"/editThing/{thing}")
    with ui.card() as card:
        print("Show thing changer:")
        thing_editor.show_thing_changer(
            card, gl_inventory.get_by_id(cast(str, thing)), gl_inventory.options
        )


def try_conversion(
    value: str, conversions: tuple[Union[Callable[[str], Any], Literal["bool"]]]
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


def new_thing():
    """Open a dialog to add a new thing."""
    thing = gl_inventory.get_id(gl_inventory.add_thing())
    print(f"Create new thing {thing}")
    ui.navigate.to(f"/editThing/{thing}")


def display_thing(card: ui.card, thing: BoxedThing) -> None:
    """Create ui elements showing information about the given thing.

    Args:
        card: the ui.card in which to display the information
        thing: thing with information
    """
    # supplying card and thing as default arguments makes it use the current
    # value instead of the value at the time of usage

    def change_card(_, c: ui.element = card, t: BoxedThing = thing):
        thing_editor.show_thing_changer(c, t, gl_inventory.options)

    with card:
        print(f"Create card {id(card)} for {thing.best('name')}.")

        with ui.row(wrap=False):
            with ui.column():
                with ui.row():
                    ui.label(text=(primary_name := thing.best("name")))
                    secondary_name = thing.get(("name", 1), None)
                    if secondary_name and (secondary_name != primary_name):
                        ui.label(text=f"({secondary_name})").style("font-size: 70%")
                    ui.button("🖉").on_click(change_card)
                if other_names := ", ".join(
                    itertools.chain(*cast(dict, thing.get("name_alt", {})).values())
                ):
                    ui.label(other_names).style("font-size: 70%")
                for description in thing.get("description", {}).values():
                    ui.markdown(description).style("font-size: 70%")
                if thing.where:
                    with ui.label(thing.where):
                        ui.tooltip(thing.location.long_name)
            if image := thing.thing.image_path():
                ui.image(image).props("width=50%").props("height=100px").props(
                    "fit='scale-down'"
                )


@ui.page("/thing/{thing}")
def show_thing(thing: str):
    """Show information about a thing."""
    navigation_row()
    card = ui.card()
    try:
        boxed_thing = gl_inventory.get_by_id(thing)
    except KeyError:
        with card:
            ui.label(
                "No such thing exists unfortunately. "
                "You can create a new one with the button above."
            )
    else:
        display_thing(card, boxed_thing)


async def list_things(
    ui_element: nicegui.ui.element, things: Iterable[BoxedThing]
) -> None:
    """Replaces content of ui_element with information about the things.

    Args:
        ui_element: Some UI element that can be changed.
        things: things to be displayed
    """
    # gives other searches 10 ms time to abort this display which might take long
    await asyncio.sleep(0.01)
    ui_element.clear()
    with ui_element:
        for thing in things:
            card = ui.card()
            display_thing(card, thing)


@ui.page("/")
def search_page() -> None:
    """Create a NiceGUI page with a search input field and search results.

    Uses global gl_inventory thing list.
    """
    print("(Re)build search page.")
    # UI container for the search results.
    results: Optional[ui.element] = None

    # Search queries (max. 1) running. Here to be cancellable by different search coroutines.
    running_queries: list[asyncio.Task] = []

    navigation_row()

    async def search(event: nicegui.events.ValueChangeEventArguments) -> None:
        """Search for cocktails as you type.

        Args:
            event: the input field change event. The new value event.value is used.
        """
        print(f"Event type: {type(event)=} with {event.value=}")
        if running_queries:
            for query in running_queries:
                query.cancel()
        sleep = asyncio.create_task(asyncio.sleep(0.5))
        running_queries.append(sleep)
        try:
            await sleep
        except asyncio.exceptions.CancelledError:
            # the next letter was already typed, do not search and rerender for this query
            return
        query = asyncio.create_task(find_things(gl_inventory, event.value))
        running_queries.append(query)
        try:
            start = time.monotonic()
            response = await query
            end = time.monotonic()
            if end - start > 0.01:
                print(f"Query {event.value}: {end - start} seconds")
        except asyncio.exceptions.CancelledError:
            pass
        else:
            if results:
                display = asyncio.create_task(list_things(results, response))
                running_queries.append(display)
                try:
                    start = time.monotonic()
                    await display
                    if end - start > 0.01:
                        print(f"Display {event.value}: {end - start} seconds")
                except asyncio.exceptions.CancelledError:
                    pass
            else:
                ui.notify("Internal error: results element is None.")

    ui.input(on_change=search).props(
        'autofocus outlined rounded item-aligned input-class="ml-3"'
    ).classes("w-96 self-center mt-24 transition-all")
    results = ui.column()


gl_options = get_options()
gl_inventory = load_data()
FAVICON_PATH = os.path.join(
    gl_options.dataDirectory, flinventory.constant.DISPLAY_RESOURCES, "favicon.ico"
)
def main_run(reload: bool=False):
    """Start the Nicegui server.


    Args:
        reload: True for reload on file changes. Set to true for development setup.
            Otherwise, leave at False as an entrypoint for a ready-to-use program.
    """
    ui.run(
        title=gl_options.title,
        favicon=FAVICON_PATH if os.path.isfile(FAVICON_PATH) else None,
        language="de",
        host=gl_options.host,
        port=gl_options.port,
        reload=reload,
    )

if __name__ in {"__main__", "__mp_main__"}:
    main_run(True)

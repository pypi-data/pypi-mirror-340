import logging
import re
from contextlib import (
    suppress,
)

from bs4 import (
    BeautifulSoup,
)
from pydantic import (
    ValidationError,
)

from labels.artifact.relationship import (
    Relationship,
)
from labels.file.location import (
    Location,
)
from labels.file.location_read_closer import (
    LocationReadCloser,
)
from labels.file.resolver import (
    Resolver,
)
from labels.model.core import (
    Language,
    Package,
    PackageType,
)
from labels.pkg.cataloger.generic.parser import (
    Environment,
)
from labels.pkg.cataloger.javascript.package import (
    package_url,
)
from labels.utils.strings import format_exception

LOGGER = logging.getLogger(__name__)

SCRIPT_DEP = re.compile(
    r"(?P<name>[^\s\/]*)(?P<separator>[-@\/])"
    r"(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*))",
)


def _get_location(location: Location, sourceline: int) -> Location:
    if location.coordinates:
        return location.model_copy(
            update={"coordinates": location.coordinates.model_copy(update={"line": sourceline})},
        )
    return location


def parse_html_scripts(
    _resolver: Resolver | None,
    _env: Environment | None,
    reader: LocationReadCloser,
) -> tuple[list[Package], list[Relationship]]:
    html = None
    with suppress(UnicodeError):
        try:
            html = BeautifulSoup(reader.read_closer, features="html.parser")
        except AssertionError:
            return [], []

    if not html:
        return [], []

    packages = []
    for script in html("script"):
        src_attribute = script.attrs.get("src")
        if not (src_attribute and src_attribute.endswith(".js")):
            continue

        matched = SCRIPT_DEP.search(src_attribute)

        if not matched:
            continue

        name = matched.group("name")
        version = matched.group("version")

        if not name or not version:
            continue

        location = _get_location(reader.location, script.sourceline)

        try:
            packages.append(
                Package(
                    name=name,
                    version=version,
                    licenses=[],
                    locations=[location],
                    language=Language.JAVASCRIPT,
                    type=PackageType.NpmPkg,
                    p_url=package_url(name, version),
                ),
            )
        except ValidationError as ex:
            LOGGER.warning(
                "Malformed package. Required fields are missing or data types are incorrect.",
                extra={
                    "extra": {
                        "exception": format_exception(str(ex)),
                        "location": location.path(),
                    },
                },
            )
            continue

    return packages, []

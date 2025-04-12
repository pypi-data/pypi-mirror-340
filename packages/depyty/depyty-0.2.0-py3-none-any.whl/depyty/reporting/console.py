from itertools import groupby
from pathlib import Path
from typing import override

from depyty.reporting.abstract import Reporter
from depyty.source_file_checking import Location, Violation


class ConsoleReporter(Reporter):
    def __init__(self, base: Path) -> None:
        self.base: Path = base

    @override
    def report(self, violations: list[Violation]) -> None:
        for distribution_name, grouped_violations in groupby(
            violations, key=lambda v: v.context.distribution_name
        ):
            print(f"{bold(distribution_name)} is missing")

            for undeclared_dependency, occurrences in groupby(
                grouped_violations, key=lambda v: v.undeclared_dependency
            ):
                print(f"\t{bold(undeclared_dependency)} which is imported in")
                for occurrence in occurrences:
                    relative_location = Location(
                        file=occurrence.location.file.relative_to(self.base),
                        line=occurrence.location.line,
                        col=occurrence.location.col,
                    )
                    print(f"\t\t{relative_location.as_location_str()}")


def bold(text: str) -> str:
    bold_prefix = "\033[1m"
    reset = "\033[0m"
    return f"{bold_prefix}{text}{reset}"

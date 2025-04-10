from __future__ import annotations

from pathlib import Path
from typing import Iterable

from sr.comp.types import ArenaName, MatchNumber, TLA

from .types import ID, RawMatch


def parse_ids(ids: str, sep: str = ',') -> list[ID]:
    return [ID(x) for x in ids.split(sep)]


def tidy(lines: Iterable[str]) -> list[str]:
    "Strip comments and trailing whitespace"
    schedule = []
    for line in lines:
        idx = line.find('#')
        if idx > -1:
            line = line[:idx]

        line = line.strip()

        if line:
            schedule.append(line)

    return schedule


def league_yaml_path(compstate_path: Path) -> Path:
    return compstate_path / 'league.yaml'


def dump_league_yaml(
    matches: dict[MatchNumber, RawMatch],
    file_path: Path,
) -> None:
    from sr.comp.cli import yaml_round_trip as yaml

    yaml.dump({'matches': matches}, dest=file_path)


def load_league_yaml(league_yaml: Path) -> dict[MatchNumber, RawMatch]:
    from sr.comp.cli import yaml_round_trip as yaml

    with open(league_yaml) as lfp:
        data = yaml.load(lfp)
        matches: dict[MatchNumber, RawMatch] = data['matches']
        return matches


def load_teams_areans(
    compstate_path: Path,
    first_match_number: MatchNumber,
) -> tuple[list[TLA], list[ArenaName], int]:
    from sr.comp import arenas, teams

    team_ids = sorted(
        x.tla
        for x in teams.load_teams(compstate_path / 'teams.yaml').values()
        if x.is_still_around(first_match_number)
    )

    arenas_yaml = compstate_path / 'arenas.yaml'
    arena_ids = sorted(arenas.load_arenas(arenas_yaml).keys())
    num_corners = len(arenas.load_corners(arenas_yaml))

    return team_ids, arena_ids, num_corners


def load_ids_schedule(
    schedule_lines: Iterable[str],
    num_arenas: int,
    teams_per_game: int,
) -> tuple[list[ID], list[list[ID]]]:
    """
    Converts an iterable of strings containing pipe-separated ids into
    a tuple: ``(ids, schedule)``. The ``ids`` is a list of unique ids
    in the order which they first appear, the ``schedule`` is a list of
    lists of ids in each line.
    """

    max_teams_per_slot = teams_per_game * num_arenas

    ids: list[ID] = []
    schedule: list[list[ID]] = []

    for match_num, match in enumerate(schedule_lines):
        match_ids = parse_ids(match, sep='|')

        uniq_match_ids = set(match_ids)
        if len(match_ids) != len(uniq_match_ids):
            raise ValueError(
                f"Match {match_num} contains the same id more than once. "
                f"(got ids {match_ids!r})",
            )

        if len(match_ids) > max_teams_per_slot:
            raise ValueError(
                f"Match {match_num} has too many ids. (got {len(match_ids)}, "
                f"can cope with {max_teams_per_slot})",
            )

        if len(match_ids) % teams_per_game != 0:
            raise ValueError(
                f"Match {match_num} has incompatible number of ids: "
                f"{len(match_ids)} is not a multiple of {teams_per_game}.",
            )

        schedule.append(match_ids)

        for id_ in match_ids:
            if id_ not in ids:
                ids.append(id_)

    return ids, schedule

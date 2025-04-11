#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from collections import namedtuple


class HostEntry(namedtuple('HostEntry', ['host', 'algorithm', 'hash'])):
    separator: str = '.'

    def __str__(self) -> str:
        return f'{self.host} {self.algorithm} {self.hash}'

    @property
    def key(self) -> str:
        return f'{self.algorithm}{self.separator}{self.hash}'


def run(args: argparse.Namespace) -> None:
    filename: Path = getattr(args, 'input', Path())
    file_path = filename.resolve()
    if not file_path.is_file():
        sys.exit(1)
    entryMap = {}

    with file_path.open(encoding='utf-8') as fp:
        for _, line in enumerate(fp):
            content = line.strip().split()
            if len(content) == 0:
                continue  # empty line -> skip
            if line[0].startswith('#') or len(content) != 3:
                print(f'Skipping line: {line}')
                continue  # comment or erroneous line -> skip
            entry = HostEntry(*content)
            entryMap.setdefault(entry.key, []).append(entry)

    compact_entry_list = []

    for key, entry_list in entryMap.items():
        host_list = []
        entry: HostEntry
        for entry in entry_list:
            for hostname in entry.host.split(','):
                if not hostname:
                    continue
                host_list.append(hostname)
        host = ','.join(sorted(host_list))
        compact_entry_list.append(HostEntry(host, *key.split(HostEntry.separator)))

    output: Path | None = getattr(args, 'output', None)
    output_lines = '\n'.join(
        map(
            str,
            sorted(
                compact_entry_list,
                key=lambda entry: (
                    entry.host[1:] if entry.host.startswith('[') else entry.host
                ),
            ),
        )
    )
    if output is None:
        for line in output_lines:
            print(line, end='')
    else:
        output_file = output.resolve()
        if output_file.is_dir():
            print('Can not write to directory.')
            sys.exit(1)
        if not output_file.parent.exists():
            output_file.parent.mkdir(parents=True)
        with output_file.open('w', encoding='utf-8') as wfp:
            wfp.writelines(output_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-i',
        '--input',
        type=Path,
        default=f'{Path("~").expanduser()}/.ssh/known_hosts',
        help='file to read',
    )
    parser.add_argument('-o', '--output', type=Path, help='file to write')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

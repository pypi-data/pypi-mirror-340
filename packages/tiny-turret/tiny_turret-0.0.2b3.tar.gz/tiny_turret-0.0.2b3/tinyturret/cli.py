#!/usr/bin/env python3
import json
import sys
import tblib

import argparse
import tabulate

from tinyturret import (
    apply_settings,
)
from tinyturret.utils import (
    get_exception_groups,
    get_exceptions,
    clear_storages,
)
import tinyturret
import traceback


def run_main(args):
    limit = args.limit if args.limit else 10

    if args.config:
        settings = json.loads(open(args.confg).read())
        apply_settings(settings)
    else:
        print('No settings file supplied, using default settings')

    if args.clear_db:
        print('Clearing all storages')
        clear_storages()
        sys.exit()

    group_infos = get_exception_groups(limit)
    if args.exceptions:
        group_idx = args.exceptions - 1
        if len(group_infos) < group_idx or len(group_infos) == 0:
            print('Exception Group index does not exists')
            sys.exit(1)

        group = group_infos[group_idx]
        print(
            'Exceptions for ', group_idx,
            'error_count =', group['info']['error_count'],
            'first_seen =', group['info']['first_seen'],
            'last_seen =', group['info']['last_seen']
        )
        print('-' * 20)
        exception_list = get_exceptions(group['group_key'], limit=2)

        for exc_struct in exception_list:
            print('timestamp =', exc_struct['timestamp'], 'exception_name', exc_struct['exception_name'])
            if exc_struct['stack_trace']:
                for trace in exc_struct['stack_trace']:
                    formatted_str = exc_struct.get('formatted_str')
                    print(trace['formatted_str'])
                    if args.locals and trace['locals']:
                        print('\tLocals:')
                        for k, v in trace['locals'].items():
                            print('\t\t', k, '=', v)
            print('-' * 20)
    else:
        headers = [
            'base_file_name',
            'exception_name',
            'exception_message',
            'error_count',
            'first_seen',
            'last_seen',
        ]
        values = []
        for idx, group in enumerate(group_infos):
            line = [idx + 1]
            for k in headers:
                val = group['info'][k]
                if k == 'base_file_name':
                    line_no = group['info']['line_number']
                    val += f':{line_no}'
                line.append(val)
            values.append(line)

        print(
            tabulate.tabulate(values, headers=['Idx'] + headers, tablefmt="rounded_outline")
        )


def add_arguments(parser):
    parser.add_argument(
        "-c", "--config", help = "json config file")
    parser.add_argument(
        "-l", "--limit", type=int, default=10, help="How many entries to display (default: %(default)s)"
    )
    parser.add_argument(
        "-e", "--exceptions", type=int, help="Show exceptions for exception group <group_idx>"
    )
    parser.add_argument(
        "-x", "--clear-db",  action="store_true", help="Clear all storages"
    )
    parser.add_argument(
        "--locals", action="store_true",help="Print locals"
    )
    return parser


def main():
    # Initialize parser
    parser = argparse.ArgumentParser()
    # Adding optional argument
    parser = add_arguments(parser)
    args = parser.parse_args()
    run_main(args)


if __name__ == '__main__':
    main()

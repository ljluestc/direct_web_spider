# encoding: utf-8
"""
Command-line argument parsing for spider scripts.
Mimics Ruby's SpiderOptions global.
"""

import argparse
import os


# Global options dictionary (mimics Ruby's SpiderOptions hash)
SpiderOptions = {
    'name': 'dangdang',
    'environment': os.environ.get('SPIDER_ENV', 'development'),
    'downloader': 'normal',
    'number': 1000
}


def parse_arguments():
    """
    Parse command-line arguments and update SpiderOptions global.

    Returns:
        dict: Updated SpiderOptions
    """
    parser = argparse.ArgumentParser(
        description='Direct Web Spider Framework - Spider Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script/run_parser.py -e production -d ty -s dangdang -n 500
  python script/run_fetcher.py -s jingdong
  python script/run_digger.py -d em -n 100
        """
    )

    parser.add_argument(
        '-s', '--name',
        type=str,
        default=SpiderOptions['name'],
        help='Spider name to run (dangdang, jingdong, tmall, newegg, suning, gome). Default: dangdang'
    )

    parser.add_argument(
        '-e', '--environment',
        type=str,
        default=SpiderOptions['environment'],
        choices=['development', 'production'],
        help='Environment to run under (development/production). Default: development'
    )

    parser.add_argument(
        '-d', '--downloader',
        type=str,
        default=SpiderOptions['downloader'],
        choices=['normal', 'ty', 'em'],
        help='Downloader type (normal=single-thread, ty=multi-thread, em=async). Default: normal'
    )

    parser.add_argument(
        '-n', '--number',
        type=int,
        default=SpiderOptions['number'],
        help='Number of records to process from database. Default: 1000'
    )

    args = parser.parse_args()

    # Update global SpiderOptions
    SpiderOptions['name'] = args.name
    SpiderOptions['environment'] = args.environment
    SpiderOptions['downloader'] = args.downloader
    SpiderOptions['number'] = args.number

    print(f"Loading {SpiderOptions['name']}'s {SpiderOptions['environment']} spider environment...")

    return SpiderOptions


# Auto-parse arguments when module is imported (mimics Ruby behavior)
if __name__ != '__main__':
    try:
        parse_arguments()
    except SystemExit:
        # If -h is passed, ArgumentParser will exit - catch it
        pass

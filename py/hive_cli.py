#!/usr/bin/python2
# -*-coding:utf-8-*-
import argparse
import subprocess
import sys
from datetime import datetime
from datetime import timedelta
import hive_driver

__author__ = 'wendale'


def main():
    time_id = (datetime.today() - timedelta(days=1)).strftime(hive_driver.DATE_ID_FORMAT)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--tid', help='base date id format:yyyyMMdd default:yesterday',
                        default=time_id, dest='time_id')
    parser.add_argument('-hivevar', '--hivevar', help='extra hive var', action='append', dest='hive_vars')

    args = parser.parse_args()
    hive_cmd = hive_driver.make_hive_args(args.time_id, args.hive_vars if args.hive_vars else [])
    print(hive_cmd)
    subprocess.call(hive_cmd, shell=True)


if __name__ == '__main__':
    main()

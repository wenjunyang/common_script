#!/usr/bin/python2
# -*-coding:utf-8-*-
import argparse
from optparse import OptionParser
import sys
import subprocess
from datetime import *
import calendar
import traceback

__author__ = 'wendale'

_VAR_NAMES = ['TIMEID',
              'TIME',
              'BEFOREDAY',
              'BEFORETIME',
              'BEFOREDAYNOFIRST',
              'MONTHID',
              'MONFIRSTDAY',
              'MONENDDAY',
              'WEEKID',
              'WEEKSTARTDAY',
              'WEEKENDDAY',
              'STARTTIMEID',
              'ENDTIMEID',
              'MONFIRSTTIME',
              'MONENDTIME',
              'CURMONFIRSTDAY',
              'WEEKSTARTTIME',
              'WEEKENDTIME',
              'BEFOREDAYNOFIRSTWK',
              'THRITYDAYAGO',
              'SIXTYDAYAGO',
              'NINETYDAYAGO',
              'DAYAGO120',
              'STARTTIME',
              'ENDTIME'
              ]

DATE_ID_FORMAT = '%Y%m%d'
DATE_STR_FORMAT = '%Y-%m-%d'
TIME_ID_FORMAT = '%Y%m%d%H%M%S'
TIME_STR_FORMAT = '%Y-%m-%d %H:%M:%S'
MONTH_ID_FORMAT = '%Y%m'


def cal_var_values(time_id):
    var_values = []
    try:
        base_time = datetime.strptime(time_id, DATE_ID_FORMAT)

        # 1. TIMEID
        var_values.append(time_id)

        # 2. TIME
        var_values.append(base_time.strftime(DATE_STR_FORMAT))

        beforeday_base_time = base_time - timedelta(days=1)
        # 3. BEFOREDAY
        var_values.append(beforeday_base_time.strftime(DATE_ID_FORMAT))

        # 4. BEFORETIME
        var_values.append(beforeday_base_time.strftime(DATE_STR_FORMAT))

        # 5. BEFOREDAYNOFIRST
        if base_time.day == 1:
            var_values.append("0")
        else:
            var_values.append(beforeday_base_time.strftime(DATE_ID_FORMAT))

        # 6. MONTHID
        var_values.append(base_time.strftime(MONTH_ID_FORMAT))

        if base_time.month == 1:
            beforemonth_start, beforemonth_end = calendar.monthrange(base_time.year - 1, 12)
            beforemonth_start_base_time = base_time.replace(year=base_time.year - 1, month=12, day=1)
            beforemonth_end_base_time = base_time.replace(year=base_time.year - 1, month=12, day=beforemonth_end)
        else:
            beforemonth_start, beforemonth_end = calendar.monthrange(base_time.year, base_time.month - 1)
            beforemonth_start_base_time = base_time.replace(month=base_time.month - 1, day=1)
            beforemonth_end_base_time = base_time.replace(month=base_time.month - 1, day=beforemonth_end)
        # 7. MONFIRSTDAY
        var_values.append(beforemonth_start_base_time.strftime(DATE_ID_FORMAT))

        # 8. MONENDDAY
        var_values.append(beforemonth_end_base_time.strftime(DATE_ID_FORMAT))

        # 9. WEEKID,注意跨年周，根据周所在哪一年天数较多决定所属哪一年
        week_int = int(base_time.strftime('%V'))
        if base_time.month == 12 and week_int < 6:
            var_values.append('%4d%02d' % (base_time.year + 1, week_int))
        elif base_time.month == 1 and week_int > 6:
            var_values.append('%4d%02d' % (base_time.year - 1, week_int))
        else:
            var_values.append(base_time.strftime('%Y%V'))

        # 10. WEEKSTARTDAY
        week_start_base_time = base_time - timedelta(days=base_time.weekday())
        var_values.append(week_start_base_time.strftime(DATE_ID_FORMAT))

        # 11. WEEKENDDAY
        week_end_base_time = base_time + timedelta(days=6 - base_time.weekday())
        var_values.append(week_end_base_time.strftime(DATE_ID_FORMAT))

        # 12. STARTTIMEID
        var_values.append(base_time.strftime(TIME_ID_FORMAT))

        # 13. ENDTIMEID
        var_values.append(base_time.replace(hour=23, minute=59, second=59).strftime(TIME_ID_FORMAT))

        month_start, month_end = calendar.monthrange(base_time.year, base_time.month)
        # 14. MONFIRSTTIME
        var_values.append(base_time.replace(day=01).strftime(DATE_STR_FORMAT))

        # 15. MONENDTIME
        var_values.append(base_time.replace(day=month_end).strftime(DATE_STR_FORMAT))

        # 16. CURMONFIRSTDAY
        var_values.append(base_time.replace(day=01).strftime(DATE_ID_FORMAT))

        # 17. WEEKSTARTTIME
        var_values.append(week_start_base_time.strftime(DATE_STR_FORMAT))

        # 18. WEEKENDTIME
        var_values.append(week_end_base_time.strftime(DATE_STR_FORMAT))

        # 19. BEFOREDAYNOFIRSTWK
        if base_time.weekday() == 0:
            var_values.append("0")
        else:
            var_values.append(beforeday_base_time.strftime(DATE_ID_FORMAT))

        # 20. THRITYDAYAGO
        var_values.append((base_time - timedelta(days=31)).strftime(DATE_ID_FORMAT))

        # 21. SIXTYDAYAGO
        var_values.append((base_time - timedelta(days=61)).strftime(DATE_ID_FORMAT))

        # 22. NINETYDAYAGO
        var_values.append((base_time - timedelta(days=91)).strftime(DATE_ID_FORMAT))

        # 23. DAYAGO120
        var_values.append((base_time - timedelta(days=121)).strftime(DATE_ID_FORMAT))

        # 24. STARTTIME
        var_values.append('"%s"' % base_time.strftime(TIME_STR_FORMAT))

        # 25. ENDTIME
        var_values.append('"%s"' % base_time.replace(hour=23, minute=59, second=59).strftime(TIME_STR_FORMAT))

        return var_values
    except Exception, e:
        traceback.print_exc()
        raise Exception('parse time id error: %s' % e.message)


def make_hive_args(time_id, hive_vars=[], hql_file=''):
    hive_var_values = cal_var_values(time_id)
    var_cmd = ' -hivevar '.join(hive_vars + [x + '=' + y for x, y in zip(_VAR_NAMES, hive_var_values)])
    if hql_file:
        return 'hive -hivevar {} -f {}'.format(var_cmd, hql_file)
    else:
        return 'hive -hivevar {}'.format(var_cmd)


def main():
    time_id = (datetime.today() - timedelta(days=1)).strftime(DATE_ID_FORMAT)

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('hql_file', help='hive sql file')
    parser.add_argument('-t', '--tid', help='base date id format:yyyyMMdd default:yesterday',
                        default=time_id, dest='time_id')
    parser.add_argument('-m', '--max', help='max try times when fail, default:1', type=int,
                         default=1, dest='max_try_times')
    parser.add_argument('-hivevar', '--hivevar', help='extra hive var', action='append', dest='hive_vars')

    args = parser.parse_args()
    try_times = 0
    hive_cmd = make_hive_args(args.time_id, args.hive_vars if args.hive_vars else [], args.hql_file)
    while try_times < args.max_try_times:
        s = subprocess.call(hive_cmd, shell=True)
        if s == 0:
            return True
        else:
            try_times += 1
    raise Exception('hive 执行出错！')


if __name__ == '__main__':
    main()

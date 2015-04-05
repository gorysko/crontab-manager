#! /usr/bin/env python
"""Command line module"""
from optparse import OptionParser

from cron_manager import *

def main():
    """Parses command line args."""
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option('-c', '--crontab', dest='crontab',
                      help='creates crontab')
    parser.add_option('-j', '--cronjob', dest='cronjob',
                      help='creates cronjob item')

    parser.add_option('--list-crontabs', dest='lc',
                      help='lists crontab')

    parser.add_option('--list-cronjobs', dest='lj',
                      help='lists cronjobs')

    parser.add_option('--current', dest='cur',
                      help='show curent')

    parser.add_option('-r', dest='rm',
                      help='removes cron')

    options, _ = parser.parse_args()


    if options.crontab is not None:
        add_cron(options.crontab)

    if options.cronjob is not None:
        cronjob = options.cronjob.split(',')
        add_crontabitem(cronjob[0], cronjob[1], cronjob[2])

    if options.lc is not None:
        status = STATUS_DISABLED
        if options.lc == 'active':
            status = STATUS_ACTIVE
        print listing(status, 'cron')

    if options.lj is not None:
        status = STATUS_DISABLED
        if options.lj == 'active':
            status = STATUS_ACTIVE
        print listing(status, 'jobs')

    if options.cur is not None:
        print listing(STATUS_RUNNING, 'cron')

    if options.rm is not None:
        remove_cron()

    if options.cronjob is not None and options.crontab is not None:
        cron = add_cron(options.crontab)
        cronjob = options.cronjob.split(',')
        cron_item = add_crontabitem(cronjob[0], cronjob[1], cronjob[2])
        link(cron_item.id, cron.id)


if __name__ == '__main__':
    main()

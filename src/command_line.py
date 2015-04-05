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

    options, _ = parser.parse_args()


    if options.crontab is not None:
        add_cron(options.crontab)

    if options.cronjob is not None:
        cronjob = options.cronjob.split(',')
        add_crontabitem(cronjob[0], cronjob[1], cronjob[2])

    if options.lc is not None:
        status = 0
        if options.lc == 'active':
            status = 1
        print listing(status, 'cron')

    if options.lj is not None:
        status = 0
        if options.lj == 'active':
            status = 1
        print listing(status, 'jobs')

    if options.cronjob is not None and options.crontab is not None:
        cron = add_cron(options.crontab)
        cronjob = options.cronjob.split(',')
        cron_item = add_crontabitem(cronjob[0], cronjob[1], cronjob[2])
        link(cron_item.id, cron.id)


if __name__ == '__main__':
    main()

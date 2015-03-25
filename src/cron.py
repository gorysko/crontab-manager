from subprocess import Popen
from subprocess import PIPE


def get_crontab():
    proc = Popen(['crontab', '-l'], stdout=PIPE)
    return proc.communicate()

def add_job(job):
    f = open('cron', 'w+')
    data = f.readlines()
    data.append(job + '\n')
    f.write(''.join(data))
    f.close()
    proc = Popen(['crontab', 'cron'], stdout=PIPE)
    return proc.communicate()

def remove_cron():
    proc = Popen(['crontab', '-r'], stdout=PIPE)
    return proc.communicate()

if __name__ == '__main__':
    print get_crontab()
    add_job('00 09 * * 1-5 echo hello')
    print get_crontab()
    print remove_cron()

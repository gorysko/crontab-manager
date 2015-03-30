# Crontab manager

This library helps you to add , edit and maintain your cronjobs. For this moment it work's via command line interface, but in some time it will be web ui supported.

## What you can do with it:

* create crontab and associate it with cronjobs
* create cronjobs and associate it with crontab
* association crontab to cronjobs is many-to-many
* you can change status of cronjobs withour deleting it and easy update your crontab
* generate crontab for it's activation
* activate crontab file
* clear crontab

## How:

* creating crontab instance whith name = 'name'

`
-c name
`

* creating  cronjob instance, whith name = 'name', schedule = '* * * * *', command = 'command'

`
-j 'name,* * * * *,command'
`

## Requirements:

* Python
* SQLite
*  and that's all

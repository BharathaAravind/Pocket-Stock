from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):

    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'PocketStock.my_cron_job' # a unique code

    def do(self):
        print 'ji'
        pass # do your thing here
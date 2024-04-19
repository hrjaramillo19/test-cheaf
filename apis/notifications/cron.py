from django_cron import CronJobBase, Schedule
from datetime import datetime
from apis.notifications.models import Alert
from apis.tasks.task import send_notification
from apis.notifications.enum import StatusEnum


class CalculatedAlerts(CronJobBase):
    """
    Crontab que se ejecuta en django para la activacion de las alertas

    se ejecuta una vez al dia
    """

    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "apis.notifications.cron.CalculatedAlerts"

    def do(self):
        alerts = Alert.objects.all()

        for alert in alerts:
            remaning_days = (alert.date_activate - datetime.now().date()).days
            days_have_passed = abs(remaning_days)
            if remaning_days <= 0:
                alert.status = StatusEnum.expire
                send_notification.delay()
            else:

                alert.number_days_activate = remaning_days
                alert.number_days_have_passed = days_have_passed

            alert.save()

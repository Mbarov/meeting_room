from django.db import models
from django.conf import settings

class Events (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'



    #checking whether the event ends on the same day as it starts
    def is_two_days(self):
        return self.start_time.day < self.end_time.day
    #location of the event on the calendar
    def coordinate(self):
        x1 = (self.start_time.weekday() + 1) *100 / 8
        y1 = ((self.start_time.hour + 6) * 60 + self.start_time.minute) * 100 / 1620 
        y2 = ((self.end_time.hour + 6  ) * 60 + self.end_time.minute) * 100 / 1620#6 - error with local time on the computer/otherwise 2
        y3 = ((self.end_time.hour + 4  ) * 60 + self.end_time.minute) * 100 / 1620#for second day
        height = y2 - y1 
        x2 = (self.start_time.weekday() + 2) *100 / 8#for second day
        height2 = 100 - y1#for second day
        return x1, y1, y2, height, x2, height2, y3

from django.db import models

# Create your models here.
# First model having full length ID, name and timezone fields
class Member(models.Model):
    fullid = models.TextField(max_length=9)
    real_name = models.TextField(max_length=50)
    tz = models.TextField(max_length=100)

    def __str__(self):
        return '%s %s %s' % (self.fullid, self.real_name, self.tz)

# @Property to return all the activity periods assosiated with a member in the ordered dict form.
# This propery will be used in MemberSerializer in serializers.py
    @property
    def activity_periods(self):
        return self.activity_period_set.all()

class Activity_period(models.Model):
    # Add a foreign key so that Activity_period model's table is linked to the Member model's table
    # Activity_period model has two fields, start_time and end_time
    member = models.ForeignKey('webapp.Member', on_delete=models.CASCADE)
    start_time = models.TextField(max_length=100)
    end_time = models.TextField(max_length=100)
    def __str__(self):
        return '%s %s' % (self.start_time, self.end_time)

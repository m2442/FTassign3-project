from rest_framework import serializers
# Import the models
from webapp.models import Activity_period, Member

# Activity_periodSerializer renders start_time and end_time fields to an API request
class Activity_periodSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)

    class Meta:
        model = Activity_period
        fields = [
         'start_time', 'end_time'
        ]
        read_only_fields = ('member',)


# MemberSerializer renders full_id, real_name, tz, and activity_periods fields to an API request
class MemberSerializer(serializers.ModelSerializer):
    # There can be more than one activity_period, so set many=True
    activity_periods = Activity_periodSerializer(many=True)
    class Meta:
        model = Member
        fields = ['fullid', 'real_name', 'tz', 'activity_periods' ]
    # We want to use this serializer for creating the data
    def create(self, validated_data):
        activity_periods = validated_data.pop('activity_periods')
        member = Member.objects.create(**validated_data)
        for activity_period in activity_periods:
            Activity_period.objects.create(**activity_period, member=member)
        return member
    # We want to use this serializer for updating the data
    def update(self, instance, validated_data):
        activity_periods = validated_data.pop('activity_periods')
        instance.fullid = validated_data.get("fullid", instance.fullid)
        instance.save()
        keep_activity_periods = []
        existing_ids = [a.id for a in instance.activity_periods]
        for activity_period in activity_periods:
            if "id" in activity_period.keys():
                if Activity_period.objects.filter(id=activity_period["id"]).exits():
                    a = Activity_period.objects.get(id=activity_period["id"])
                    a.text = activity_period.get('text', a.text)
                    a.save()
                    keep_activity_periods.append(a.id)
                else:
                    continue
            else:
                a = Activity_period.objects.create(**activity_period, member=instance)
                keep_activity_periods.append(a.id)
        for activity_period in instance.activity_periods:
            if activity_period.id not in keep_activity_periods:
                activity_period.delete()
        return instance

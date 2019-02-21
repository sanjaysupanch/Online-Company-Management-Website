from rest_framework import serializers
from django.contrib.auth.models import User
from put_calendar.models import check_date
from rest_framework import generics



class check_dateSerializer(serializers.ModelSerializer):


	class Meta:
		model=check_date
		fields=('id','date', 'work_title', 'user',)



class UserSerializer(serializers.ModelSerializer):
	check_dates = check_dateSerializer(many=True)

	class Meta:
		model = User
		fields = (
        	'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
			)

	def create(self, validated_data):
		checkdates12_data = validated_data.pop('check_dates')
		user = User.objects.create(**validated_data)
		for checker_data in checkdates12_data:
			check_date.objects.create(user=user, **checker_data)
		return user

	def update(self, instance, validated_data):
		checkdates12_data = validated_data.pop('check_dates')
		check_dates123 = (instance.check_dates).all()
		check_dates123 = list(check_dates)
		instance.username = validated_data.get('username', instance.username)
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.password = validated_data.get('password', instance.password)
		instance.save()

		for checker_data in checkdates12_data:
			checker123 = check_dates123.pop(0)
			checker123.date = checker_data.get('date', checker123.name)
			checker123.work_title = checker_data.get('release_date', checker.work_title)
			checker123.save()
		return instance



		

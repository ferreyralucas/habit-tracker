import factory
from django.contrib.auth.models import User
from .models import Habit, HabitRecord
from faker import Faker

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.email())


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    user = factory.SubFactory(UserFactory)
    name = factory.LazyAttribute(lambda _: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda _: faker.text())
    target = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=10))
    target_period = factory.Iterator(['daily', 'weekly', 'monthly'])


class HabitRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HabitRecord

    habit = factory.SubFactory(HabitFactory)
    date = factory.LazyAttribute(lambda _: faker.date())
    completion = factory.LazyAttribute(lambda _: faker.random_int(min=1, max=10))
    note = factory.LazyAttribute(lambda _: faker.text())

from datetime import date, timedelta
from faker import Factory
from .models import Choice, Answer, Question
import factory
import factory.fuzzy


faker = Factory.create()


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    text = factory.LazyAttribute(lambda _: faker.word())


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.LazyAttribute(lambda _: faker.text())

    @factory.post_generation
    def choices(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for choice in extracted:
                self.choices.add(choice)

        for _ in range(4):
            self.choices.add(ChoiceFactory())


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    created = factory.fuzzy.FuzzyDate(
        start_date=(date.today() + timedelta(days=-10)), end_date=date.today()
    )
    question = factory.SubFactory(QuestionFactory)
    choice = factory.SubFactory(ChoiceFactory)

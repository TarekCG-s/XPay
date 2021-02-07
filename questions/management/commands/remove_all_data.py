from django.core.management.base import BaseCommand
from questions.factories import QuestionFactory, AnswerFactory
from questions.models import Question, Answer, Choice
import random


class Command(BaseCommand):
    help = 'Deletes all data'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Choice.objects.all().delete()

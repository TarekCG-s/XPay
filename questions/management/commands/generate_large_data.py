from django.core.management.base import BaseCommand
from questions.factories import QuestionFactory, AnswerFactory
from questions.models import Question
import random


class Command(BaseCommand):
    help = 'Generate Large numbers of questions and answers'

    def handle(self, *args, **kwargs):
        questions = QuestionFactory.create_batch(size=100)
        for i in range(100):
            AnswerFactory.create_batch(size=100, question=questions[i], choice=questions[i].choices.last())


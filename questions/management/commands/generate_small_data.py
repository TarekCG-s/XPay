from django.core.management.base import BaseCommand
from questions.factories import QuestionFactory, AnswerFactory
from questions.models import Question
import random


class Command(BaseCommand):
    help = 'Generate small numbers of questions and answers'

    def handle(self, *args, **kwargs):
        questions = QuestionFactory.create_batch(size=10)
        for i in range(10):
            AnswerFactory.create_batch(size=10, question=questions[i], choice=questions[i].choices.last())


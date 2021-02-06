from django.db import models
from django.core.exceptions import ValidationError


class Choice(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField()
    choices = models.ManyToManyField(Choice, related_name="questions")

    def __str__(self):
        return self.text


class Answer(models.Model):
    created = models.DateField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return f"{self.question} - {self.choice}"

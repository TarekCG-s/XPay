from django.db import models

class Choice(models.Model):
    text = models.CharField(max_length=100)

class Question(models.Model):
    text = models.TextField()
    choices = models.ManyToManyField(Choice, related_name="questions")

class Answer(models.Model):
    created = models.DateField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers")

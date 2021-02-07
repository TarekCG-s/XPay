from dateutil import parser
from django.db.models import Count
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Answer, Question
from .permissions import IsNotSuperUser


class AnswersViewset(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, IsNotSuperUser)

    def get(self, request):
        questions_params = {}
        answers_params = {}

        from_date = self.request.query_params.get("from_date")
        if from_date:
            try:
                from_date = parser.parse(from_date)
                questions_params["answers__created__gte"] = from_date
                answers_params["created__gte"] = from_date
            except:
                return Response("Invalid From Date", 400)

        to_date = self.request.query_params.get("to_date")
        if to_date:
            try:
                to_date = parser.parse(to_date)
                questions_params["answers__created__lte"] = to_date
                answers_params["created__lte"] = to_date
            except:
                return Response("Invalid To Date", 400)

        answers = {
            obj.id: obj
            for obj in Answer.objects.filter(**answers_params).select_related("choice")
        }

        questions = (
            Question.objects.filter(**questions_params)
            .prefetch_related("answers")
            .values("text", "answers__created")
            .annotate(answers_count=Count("answers__id"), answers_ids=ArrayAgg("answers"))
        )

        questions_counts = (
            Answer.objects.filter(**answers_params)
            .values("created")
            .order_by("-created")
            .annotate(Count("question", distinct=True))
        )

        data = {}
        for date in questions_counts:
            data[str(date.get("created"))] = {
                "questions_count": date.get("question__count")
            }

        for question in questions:
            if question.get("answers__created"):
                related_answers = map(
                    lambda x: {
                        "id": x,
                        "choice": {"id": answers[x].choice.id},
                        "text": answers[x].choice.text,
                    },
                    question.get("answers_ids"),
                )
                data[str(question.get("answers__created"))][question.get("text")] = {
                    "answers_count": question.get("answers_count"),
                    "answers": related_answers,
                }

        return Response(data)

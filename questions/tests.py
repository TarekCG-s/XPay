from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import QuestionFactory, AnswerFactory
from datetime import datetime, timedelta


class AnswersViewsetTests(APITestCase):
    def setUp(self):
        self.url = reverse("answers")
        self.user = User.objects.create(
            username="user", password="password", is_staff=True
        )

    def test_valid_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser(self):

        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_staff_user(self):
        self.user.is_staff = False
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetching_answers(self):
        today = datetime.today()
        question1 = QuestionFactory.create()
        question2 = QuestionFactory.create()
        AnswerFactory.create_batch(
            size=3, created=today, question=question1, choice=question1.choices.last()
        )
        AnswerFactory.create(
            created=today, question=question2, choice=question2.choices.first()
        )

        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        today_str = str(datetime.date(today))
        self.assertIsNotNone(data.get(today_str))
        self.assertEqual(data.get(today_str).get("questions_count"), 2)
        self.assertEqual(
            data.get(today_str).get(question1.text).get("answers_count"), 3
        )
        self.assertEqual(
            data.get(today_str).get(question2.text).get("answers_count"), 1
        )

    def test_query_params(self):
        today = datetime.today()
        week_before = today + timedelta(days=-7)
        month_before = today + timedelta(days=-30)
        question1 = QuestionFactory.create()
        AnswerFactory.create_batch(
            size=3, created=today, question=question1, choice=question1.choices.last()
        )
        AnswerFactory.create_batch(
            size=2,
            created=week_before,
            question=question1,
            choice=question1.choices.last(),
        )
        AnswerFactory.create(
            created=month_before, question=question1, choice=question1.choices.last()
        )

        self.client.force_login(self.user)
        response = self.client.get(
            self.url, {"from_date": str(datetime.date(week_before))}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data.items()), 2)
        self.assertIsNotNone(data.get(str(datetime.date(today))))
        self.assertIsNotNone(data.get(str(datetime.date(week_before))))
        self.assertIsNone(data.get(str(datetime.date(month_before))))

        response = self.client.get(
            self.url, {"to_date": str(datetime.date(week_before))}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data.items()), 2)
        self.assertIsNone(data.get(str(datetime.date(today))))
        self.assertIsNotNone(data.get(str(datetime.date(week_before))))
        self.assertIsNotNone(data.get(str(datetime.date(month_before))))

        response = self.client.get(
            self.url,
            {
                "to_date": str(datetime.date(week_before)),
                "from_date": str(datetime.date(week_before)),
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(len(data.items()), 1)
        self.assertIsNone(data.get(str(datetime.date(today))))
        self.assertIsNotNone(data.get(str(datetime.date(week_before))))
        self.assertIsNone(data.get(str(datetime.date(month_before))))

import random

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


def limit_content_type_choices():
    problem_subclasses = Problem.__subclasses__()
    content_types = ContentType.objects.get_for_models(*problem_subclasses).values()
    return {"id__in": {content_type.id for content_type in content_types}}


class ProblemText(models.Model):
    """TODO
    :param content_type:
    :type content_type: class:`django.contrib.contenttypes.models.ContentType
    :param question:
    :type question: str, optional
    :param answer:
    :type answer: str, optional
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return f"{self.content_type.name}: {self.question} / {self.answer}"

    def render(self, data):
        question = self.question.format(**data)
        answer = self.answer.format(**data)
        return question, answer


class GeneratedDataIncorrect(Exception):
    pass


class Problem(models.Model):
    """TODO
    :param quiz: Pertaining to a quiz.
    :type quiz: class:`quizzes.Quiz`
    :param content_type:
    :type content_type: class:`django.contrib.contenttypes.models.ContentType
    :param text:
    :type text: class:`problems.ProblemText`
    """

    quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        limit_choices_to=limit_content_type_choices,
    )
    text = models.ForeignKey("problems.ProblemText", on_delete=models.PROTECT)

    class Meta:
        default_related_name = "problems"

    def __str__(self):
        return f"{self.quiz}: {self.content_type.name}"

    def clean(self):
        """TODO
        :raises ValidationError:
        """
        if issubclass(Problem, type(self)):
            raise ValidationError("Problems must have a non-trivial generator")
        self.content_type = ContentType.objects.get_for_model(type(self))
        if hasattr(self, "text") and self.content_type != self.text.content_type:
            raise ValidationError("Generators of the problem and its text must match")

    def save(self, *args, **kwargs):
        """TODO"""
        self.content_type = ContentType.objects.get_for_model(type(self))
        super().save(*args, **kwargs)

    def downcast(self):
        """TODO
        :return:
        :retype: class:`django.contrib.contenttypes.models.ContentType
        """
        content_type = self.content_type
        if content_type.model_class() == type(self):
            return self
        return content_type.get_object_for_this_type(problem_ptr_id=self.id)

    def generate(self):
        """TODO
        :raises NotImplementedError:
        """
        raise NotImplementedError

    def validate(self, condition):
        """TODO
        :param condition:
        :type condition: bool
        :raises GeneratedDataIncorrect: If codition is `False`
        """
        if not condition:
            raise GeneratedDataIncorrect

    def generate_data(self, seed):
        """TODO
        :raises GeneratedDataIncorrect:
        :return:
        :retype:
        """
        random.seed(seed)
        generator = self.downcast()
        while True:
            try:
                return generator.generate()
            except GeneratedDataIncorrect:
                pass

    def generate_everything(self, student=None):
        """TODO

        :param student:
        :type student:
        :return:
        :retype:
        """
        seed = (self.id, None if student is None else student.id)
        data = self.generate_data(seed)
        question, answer = self.text.render(data)
        return data, question, answer


class ProstoBesedilo(Problem):
    """TODO
    :param vprasanje:
    :type vprasanje: str
    :param odgovor:
    :type odgovor: str
    """

    vprasanje = models.TextField()
    odgovor = models.TextField()

    def generate(self):
        """TODO"""
        return {
            "vprasanje": self.vprasanje,
            "odgovor": self.odgovor,
        }


class KrajsanjeUlomkov(Problem):
    """This class represents an exercise of reducing fractions to lowest terms.

    :param najvecji_stevec: Greatest possible numerator.
    :type najvecji_stevec: int
    :param najvecji_imenovalec: Greatest possible denominator.
    :type najvecji_imenovalec: int
    :param najvecji_faktor: Greatest possible factor the numerator and the denominator are multiplied by. Factor to be reduced by the student.
    :type najvecji_faktor: int
    """

    najvecji_stevec = models.PositiveSmallIntegerField()
    najvecji_imenovalec = models.PositiveSmallIntegerField()
    najvecji_faktor = models.PositiveSmallIntegerField()

    def generate(self):
        """TODO
        :return:
        :retype: dictionary
        """
        stevec = random.randint(1, self.najvecji_stevec)
        imenovalec = random.randint(1, self.najvecji_imenovalec)
        faktor = random.randint(1, self.najvecji_faktor)
        return {
            "okrajsan_stevec": stevec,
            "okrajsan_imenovalec": imenovalec,
            "neokrajsan_stevec": faktor * stevec,
            "neokrajsan_imenovalec": faktor * imenovalec,
        }


class IskanjeNicelPolinoma(Problem):
    """This class represents an exercise of calculating the roots of a polynomial.

    :param stevilo_nicel: Number of roots of featured polynomials.
    :type stevilo_nicel: int
    :param velikost_nicel: Magnitude of roots of featured polynomials.
    :type velikost_nicel: int
    """

    stevilo_nicel = models.PositiveSmallIntegerField()
    velikost_nicle = models.PositiveSmallIntegerField()

    def generate(self):
        """TODO
        :return:
        :retype: dictionary
        """
        nicla = random.randint(1, self.velikost_nicle)
        if self.stevilo_nicel % 2 == 0:
            nicle = {nicla, -nicla}
        else:
            nicle = {nicla}
        polinom = f"x^{self.stevilo_nicel} - {nicla ** self.stevilo_nicel}"
        return {"nicle": nicle, "polinom": polinom}

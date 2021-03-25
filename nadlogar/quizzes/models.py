from django.db import models


class Quiz(models.Model):
    """
    :param name: The title of the quiz. A string no longer than 255 characters.
    :type name: str
    :param date: The date to be displayed on the quiy. Ordinarily when the quiz will take place.
    :type date: datetime
    :param description: Quit description.
    :type description: str, optional
    :param student_group: The group to which the quiz is asigned.
    :type student_group: class:`students.StudentGroup`
    """

    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True)
    student_group = models.ForeignKey("students.StudentGroup", on_delete=models.CASCADE)

    class Meta:
        ordering = ["date", "name"]
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"{self.name} ({self.date})"

    def generate_everything(self):
        """
        :return: Dictionary of :class:`students.Student` objects as keys and lists of :class:`problems.Problem` objects as values.
        :retype: dictionary
        """
        students = self.student_group.students.all()
        student_quizzes = {student: [] for student in students}
        for problem in self.problems.all():
            for student in students:
                student_quizzes[student].append(problem.generate_everything(student))
        return student_quizzes

    def problem_examples(self):
        """
        :return: List of lists of :class:`problems.Problem` objects, quiz date, and :class:`quizzes.Quiz` atributes question and answer.
        :retype: list
        """
        # TODO Opis returna je nerode. Sploh za question and answer.
        examples = []
        for problem in self.problems.all():
            data, question, answer = problem.generate_everything()
            examples.append((problem, data, question, answer))
        return examples

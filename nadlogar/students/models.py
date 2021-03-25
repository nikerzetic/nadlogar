from django.db import models


class StudentGroup(models.Model):
    """A class for grouping students. When creating a :class:`Quiz` you must asing it a :class:`StudentGroup`. You can only asign :class:`Quiz` classes to :class:`StudentGroup` classes, and not individual :class:`Student` classes.

    :param name: A string of no more than 255 characters that represents a group's name.
    :type name: str
    """

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Method that responds to a str() call."""
        return self.name


class Student(models.Model):
    """A class that represents a single student.
    :param name: A string of no more than 255 characters that represents a student's name.
    :type name: str
    :param group: A group the student belongs to. Each student can only belong to one group.
    :type group: class:`students.StudentGroup`
    """

    name = models.CharField(max_length=255)
    group = models.ForeignKey("students.StudentGroup", on_delete=models.CASCADE)

    class Meta:
        """Meta class that defines the name to use for the reverse filter name, and the ordering for the class :class:`Student`."""

        default_related_name = "students"
        ordering = ["group", "name"]

    def __str__(self):
        """Method that responds to a str() call."""
        return f"{self.name} ({self.group})"

from django.db import models


class Task(models.Model):
    LOW = 'Низкий'
    MEDIUM = 'Средний'
    HIGH = 'Высокий'
    PRIORITY_CHOICES = [
        (LOW, 'Низкий'),
        (MEDIUM, 'Средний'),
        (HIGH, 'Высокий'),
    ]

    NOT_DONE = 'Не выполнена'
    DONE = 'Выполнена'
    STATUS_CHOICES = [
        (NOT_DONE, 'Не выполнена'),
        (DONE, 'Выполнена'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_DONE)

    def switch_status(self):
        if self.status in [self.NOT_DONE, self.DONE]:
            self.status = self.DONE if self.status == self.NOT_DONE else self.NOT_DONE
            self.save(update_fields=['status'])

    def __str__(self):
        return f'{self.title} ({self.status})'

    class Meta:
        ordering = ['-due_date']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

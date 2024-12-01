from django.core.management.base import BaseCommand
from django.db.models import Q
from datetime import datetime
from tasks.models import Task


class Command(BaseCommand):
    help = 'Менеджер задач через консоль'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Действие: list, add, update, delete, search')

    def handle(self, *args, **options):
        action = options['action']

        actions = {
            'list': self.list_tasks,
            'add': self.add_task,
            'update': self.update_task,
            'delete': self.delete_task,
            'search': self.search_tasks,
        }

        if action in actions:
            actions[action]()
        else:
            self.stdout.write(self.style.ERROR('Неверное действие'))

    def list_tasks(self):

        tasks = Task.objects.all()
        if not tasks:
            self.stdout.write(self.style.WARNING('Задач нет'))
            return
        for task in tasks:
            self.stdout.write(
                f"""
                ID: {task.id}
                Название: {task.title}
                Описание: {task.description or 'Нет описания'}
                Категория: {task.category or 'Не указана'}
                Срок: {task.due_date}
                Приоритет: {task.get_priority_display()}
                Статус: {task.get_status_display()}
                {'=' * 30}
                """
            )

    def add_task(self):
        title = input('Название задачи: ')
        description = input('Описание: ') or None
        category = input("Категория: ") or None
        due_date = self.get_valid_date("Дата выполнения (формат YYYY-MM-DD): ")
        priority = self.get_priority_choices()

        task = Task.objects.create(
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
        )
        self.stdout.write(self.style.SUCCESS(f'Задача "{task.title}" добавлена'))

    def update_task(self):
        try:
            task_id = int(input('Введите ID задачи: '))
        except ValueError:
            self.stdout.write(self.style.ERROR("ID задачи должен быть числом"))
            return

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("Задача не найдена"))
            return

        print('1. Изменить статус')
        print('2. Обновить другие поля')

        update_choice = input('Выберите действие: ')

        if update_choice == '1':
            task.switch_status()
            self.stdout.write(self.style.SUCCESS("Статус обновлен"))
        elif update_choice == '2':
            task.title = input("Введите новое название: ") or task.title
            task.description = input('Введите новое описание: ') or task.description
            task.category = input('Введите новую категорию: ') or task.category
            task.due_date = self.get_valid_date("Введите новую дату выполнения (формат YYYY-MM-DD): ") or task.due_date
            task.priority = self.get_priority_choices(default=task.priority)
            task.save()
            self.stdout.write(self.style.SUCCESS("Задача обновлена"))

    def delete_task(self):
        try:
            task_id = int(input('Введите ID задачи: '))
        except ValueError:
            self.stdout.write(self.style.ERROR("ID задачи должен быть числом"))
            return

        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            self.stdout.write(self.style.SUCCESS(f'Задача с ID {task_id} удалена'))
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR("Задача не найдена"))

    def search_tasks(self):
        keyword = input('Введите ключевое слово: ').strip()
        if not keyword:
            self.stdout.write(self.style.WARNING('Введите ключевое слово'))
            return
        tasks = Task.objects.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__icontains=keyword)
        )
        if not tasks.exists():
            self.stdout.write(self.style.WARNING('Задачи не найдены'))
            return
        self.stdout.write(f"Найдено задач: {tasks.count()}\n{'=' * 30}")
        for task in tasks:
            self.stdout.write(
                f"""
                ID: {task.id}
                Название: {task.title}
                Описание: {task.description or 'Нет описания'}
                Категория: {task.category or 'Не указана'}
                Срок: {task.due_date}
                Приоритет: {task.get_priority_display()}
                Статус: {task.get_status_display()}
                {'=' * 30}
                """
            )

    def get_valid_date(self, prompt):
        while True:
            try:
                date_str = input(prompt)
                if not date_str:
                    print("Дата не может быть пустой. Попробуйте снова.")
                    continue
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print('Некорректный формат. Попробуйте снова.')

    def get_priority_choices(self, default=Task.LOW):
        priority_choices = {
            '1': Task.LOW,
            '2': Task.MEDIUM,
            '3': Task.HIGH,
        }

        print('Приоритет:')
        print('1. Низкий')
        print('2. Средний')
        print('3. Высокий')
        choice = input('Выберите приоритет: ')
        return priority_choices.get(choice, default)

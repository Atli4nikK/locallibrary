from django.db import models
from django.urls import reverse  # Используется для генерации URL путем изменения шаблонов URL
import uuid  # Требуется для уникальных экземпляров книги


# Create your models here.
# Модель жанра
class Genre(models.Model):
    """
    Модель, представляющая жанр книги (например, Фантастика, без жанра).
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги (например Фантастика, поэзия и др.)")

    # Метод возвращает имя жанра, определенного конкретной записью
    def __str__(self):
        """
        Строка для представления объекта Model (на сайте администратора и т. д.)
        :return:
        """
        return self.name


# Модель книги
class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретный физический экземпляр или копию книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Используется внешний ключ, потому что у книги может быть только один автор
    # (в нашей реализации, на практике у книги может быть несколько авторов), но у авторов может быть несколько книг
    # Автор как строка, а не объект, потому что он еще не был объявлен в файле
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='''13 Character <a href="https://www.isbn-international.org/content/what-isbn">
                                      ISBN number</a>''')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для этой книги")

    # ManyToManyField используется потому, что жанр может содержать много книг. Книги могут охватывать многие жанры.
    # Жанровый класс уже определен, поэтому мы можем указать объект выше.

    def __str__(self):
        """
        Строка для представления объекта Model.
        :return:
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретному экземпляру книги.
        :return:
        """
        return reverse('book-detail', args=[str(self.id)])


# Модель экземпляра книги
class BookInstance(models.Model):
    """
    Модель, представляющая конкретную копию книги (то есть, которая может быть взята из библиотеки).

    UUIDField используется для поля id, чтобы установить его как primary_key для этой модели. Этот тип поля выделяет
    глобальное уникальное значение для каждого экземпляра (по одному для каждой книги, которую вы можете найти в
    библиотеке).

    DateField используется для данных due_back (при которых ожидается, что книга появится после заимствования или
    обслуживания). Это значение может быть blank или null (необходимо, когда книга доступна). Метаданные модели
    (Class Meta) используют это поле для упорядочивания записей, когда они возвращаются в запросе.

    status - это CharField, который определяет список choice/selection. Как вы можете видеть, мы определяем кортеж,
    содержащий кортежи пар ключ-значение и передаем его аргументу выбора. Значение в key/value паре - это отображаемое
    значение, которое пользователь может выбрать, а ключи - это значения, которые фактически сохраняются, если выбрана
    опция. Мы также установили значение по умолчанию «m» (техническое обслуживание), поскольку книги изначально будут
    созданы недоступными до того, как они будут храниться на полках.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="""Уникальный идентификатор для этой конкретной книги во всей библиотеке""")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """
        Строка для представления объекта Model
        Модель __str __ () представляет объект BookInstance, используя комбинацию его уникального идентификатора и
        связанного с ним заголовка книги.
        :return:
        """
        return '{0} ({1})'.format(self.id, self.book.title)


# Модель автора
class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретному экземпляру автора.
        :return:
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления объекта Model.
        :return:
        """
        return '{0}, {1}'.format(self.last_name, self.first_name)


# Модель естественного языка книги
class Language(models.Model):
    """
    Модель, представляющая язык (например, английский, французский, японский и т. д.)
    """
    name = models.CharField(max_length=200,
                            help_text="Введите естественный язык книги (например, английский, французский и т. д.)")

    def __str__(self):
        """
        Строка для представления объекта Model
        :return:
        """
        return self.name

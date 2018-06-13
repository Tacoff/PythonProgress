from django.db import models
from django.utils import timezone
# Create your models here.
# relationship - many-to-one


class Manufacturer(models.Model):
    # get_[location]_display() to get the display name
    choice = (
        ('n', '北'),
        ('s', '南'),
        ('w', '西'),
        ('e', '东'),
    )
    name = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=20, choices=choice, default='n')


class Car(models.Model):
    brand = models.CharField("品牌", max_length=10)
    production_date = models.DateTimeField("生产日期", auto_now=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


# relationship - many-to-many
class Article(models.Model):
    name = models.CharField(max_length=10)
    content = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.username


# relationship - many-to-many-through
# especially notice the through and through_fields
# membership is the relationship table which record the ship information, there are two foreignkey,
# if exists more, you should definite the fields with through_fields args, also you need modify the
# other foreign key with different related_name

# notice the order of through_fields
# through_fields accepts a 2-tuple ('field1', 'field2'), where field1 is the name of the foreign
# key to the model (means myself, omg unclear) the ManyToManyField is defined on (group in this case), and field2 the name of the
# foreign key to the target model (person in this case).
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership', through_fields=("group", "person"))

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)
    invite_reason = models.CharField(max_length=64)
    inviter = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="membership_invites")
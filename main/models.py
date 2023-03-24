from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader import fields


class Post(models.Model):
    title = models.CharField(max_length=128)
    content = fields.RichTextUploadingField()
    categories = models.ManyToManyField(to='Category')
    author = models.ForeignKey(to='User', on_delete=models.CASCADE)

class Reply(models.Model):
    author = models.ForeignKey(to='User', on_delete=models.CASCADE)
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    content = models.TextField()


class Category(models.Model):
    tank = 'TK'
    healer = 'HL'
    damage_dealer = 'DD'
    tradesman = 'TM'
    guild_master = 'GM'
    quest_giver = 'QG'
    blacksmith = 'BS'
    tanner = 'TN'
    potion_master = 'PM'
    spell_master = 'SM'
    
    OPTIONS = (
        (tank, 'Танки'),
        (healer, 'Хилы'),
        (damage_dealer, 'ДД'),
        (tradesman, 'Торговец'),
        (guild_master, 'Гилдмастер'),
        (quest_giver, 'Квестгивер'),
        (blacksmith, 'Кузнец'),
        (tanner, 'Кожевник'),
        (potion_master, 'Зельевар'),
        (spell_master, 'Мастер заклинаний')
    )
    
    name = models.CharField(max_length=2, choices=OPTIONS)
from django.db import models
from django.core.validators import RegexValidator

# Universal variables
alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Word Collection name can only be alphanumeric.')

# Create your models here.

class WordCollection(models.Model):
    word_collection = models.CharField(max_length=30, validators=[alphanumeric])

    def __str__(self):
        return self.word_collection

class Word(models.Model):
    word_collections = models.ForeignKey(WordCollection, on_delete = models.CASCADE)
    word = models.CharField(max_length = 30)

    def __str__(self):
        return self.word

class CollectionGrid(models.Model):
    word_collection = models.ForeignKey(WordCollection, on_delete = models.CASCADE)
    grid_map_key = models.IntegerField(unique=True)
    difficulty = models.IntegerField()
    grid_size = models.IntegerField()

    def __str__(self):
        return f'{self.word_collection}-{self.grid_map_key}-{self.difficulty}-{self.grid_size}'

class GridMap(models.Model):
    grid_map_key = models.ForeignKey(CollectionGrid, to_field='grid_map_key', db_column='grid_map_key', on_delete=models.CASCADE)
    cell = models.CharField(max_length=7)
    letter = models.CharField(max_length=1)
    word_key = models.IntegerField()

    def __str__(self):
        return self.cell
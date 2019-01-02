from django.db import models
from languages.fields import LanguageField

# Create your models here.

class Collections(models.Model):
	collection_name = models.CharField(max_length=200)
	collection_link = models.URLField(blank=True)
	language = LanguageField(blank=True)
	desc = models.TextField(blank=True)
	weights_path = models.CharField(max_length=200, blank='True')
	kdtree_path = models.CharField(max_length=200, blank='True')
	page2word_path = models.CharField(max_length=200, blank='True')
	wrd_pos_fpath = models.CharField(max_length=200, blank='True')
	words_path = models.CharField(max_length=200, blank='True')
	demo_path = models.CharField(max_length=200, blank='True')

	def __str__(self):
		return self.collection_name
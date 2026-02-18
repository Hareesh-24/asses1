from django.db import models


class Recipe(models.Model):
    cuisine= models.TextField(max_length=100, blank=True)
    title= models.TextField(max_length=100, blank=True)
    rating= models.FloatField(null=True, blank=True)
    prep_time= models.IntegerField(null=True, blank=True, help_text="Minutes")
    cook_time= models.IntegerField(null=True, blank=True, help_text="Minutes")
    total_time= models.IntegerField(null=True, blank=True, help_text="Minutes")
    description= models.TextField(blank=True)   
    nutrients= models.JSONField(blank=True,null=True)
    serves= models.TextField(null=True, blank=True)      

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.title

    
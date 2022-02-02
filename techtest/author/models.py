from django.db import models

class Author(models.Model):
    """Author of the books"""
    first_name = models.CharField(max_length=40, help_text="First name")
    last_name = models.CharField(max_length=40, help_text="Last name")

    def __str__(self):
        return f"<Author id={self.id} first_name={self.first_name} last_name={self.last_name}>"

    class Meta:
        unique_together = (("first_name", "last_name"),)
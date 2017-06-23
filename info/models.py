from django.db import models


class ClubTag(models.Model):
    tag_name = models.CharField(max_length=50, null=True, default=True)

    def __str__(self):
        return self.tag_name



from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    owners = models.ManyToManyField(
        User
    )
    date_added = models.DateField(auto_now_add=True)

    # Circular import issue -- use appname.ClassName as a string for workaround
    # Reverse query name issue -- add related_name for workaround
    branches = models.ForeignKey(
        'branch.Branch',
        related_name='children',
        blank=True, null=True, on_delete=models.SET_NULL
    )


    def __str__(self):
        return self.name
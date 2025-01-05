from django.db import models

# Create your models here.
class Repository(models.Model):
    name = models.CharField(max_length=200)
    project_id = models.IntegerField(unique=True)
    last_assessed = models.DateTimeField(auto_now=True)
    variables_protected = models.BooleanField()
    runners_secure = models.BooleanField()
    status = models.CharField(max_length=50, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return self.name

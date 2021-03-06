from django.contrib.auth.models import User
from django.db import models

class Request(models.Model):
    path = models.CharField(max_length=1024, help_text = "The relative url to request. Ex: '/search?q=test'", verbose_name = "Request Path")
    login_as_user = models.ForeignKey(User, blank = True, help_text = "User to login-as. Blank for anonymous", null = True)
    comments = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __unicode__(self):
        out = self.path
        for rule in self.requestrule_set.all():
            out += ", " + str(rule)
        return out

class RequestRule(models.Model):
    OPERATOR_CHOICES = (
        ('contains', 'contains'),
        ('!contains', 'does not contain'),
        ('=', 'equals'),
        ('!=', 'not equal'),
        ('<', 'less than'),
        ('>', 'greater than')
    )

    request = models.ForeignKey(Request)
    target = models.CharField(max_length = 255, verbose_name = "Where to look")
    operator = models.CharField(max_length = 255, choices = OPERATOR_CHOICES)
    value = models.CharField(max_length = 255, verbose_name = "What to look for")

    @property
    def display_operator(self):
        try:
            operator = dict(RequestRule.OPERATOR_CHOICES)[self.operator]
            return operator
        except:
            return self.operator

    def __unicode__(self):
        return "%s %s '%s'" % (self.target, self.display_operator, self.value)

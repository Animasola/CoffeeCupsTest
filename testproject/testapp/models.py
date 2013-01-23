from django.db import models


class PersonalInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    last_name = models.CharField(max_length=70, verbose_name='Last Name')
    birth_date = models.DateField(auto_now=False, auto_now_add=False,
                verbose_name='Date of birth')
    bio = models.TextField(verbose_name='Bio')
    email = models.EmailField(max_length=75, verbose_name='Email')
    jabber = models.CharField(max_length=50, verbose_name='Jabber')
    skype = models.CharField(max_length=50, verbose_name='Skype')
    other_contacts = models.TextField(verbose_name='Other contacts')

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Fertilizer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    name = models.CharField('Название',max_length=100)
    nh4 = models.FloatField('% NH4', default=0)
    no3 = models.FloatField('% NO3', default=0)
    p2o5 = models.FloatField('% P2O5', default=0)
    k2o = models.FloatField('% K2O', default=0)
    cao = models.FloatField('% CaO', default=0)
    mgo = models.FloatField('% MgO', default=0)
    s = models.FloatField('% S', default=0)
    cl = models.FloatField('% Cl', default=0)
    fe = models.FloatField('% Fe', default=0)
    mn = models.FloatField('% Mn', default=0)
    b = models.FloatField('% B', default=0)
    zn = models.FloatField('% Zn', default=0)
    cu = models.FloatField('% Cu', default=0)
    mo = models.FloatField('% Mo', default=0)
    co = models.FloatField('% Co', default=0)
    si = models.FloatField('% Si', default=0)

    def __str__(self):
        return self.name
    
class P_profile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    name = models.CharField('Название',max_length=100)
    nh4 = models.FloatField('NH4, мг/л', default=0)
    no3 = models.FloatField('NO3, мг/л', default=0)
    p = models.FloatField('P, мг/л', default=0)
    k = models.FloatField('K, мг/л', default=0)
    ca = models.FloatField('Сa, мг/л', default=0)
    mg = models.FloatField('Mg, мг/л', default=0)
    s = models.FloatField('S, мг/л', default=0)
    cl = models.FloatField('Cl, мг/л', default=0)
    fe = models.FloatField('Fe, мкг/л', default=0)
    mn = models.FloatField('Mn, мкг/л', default=0)
    b = models.FloatField('B, мкг/л', default=0)
    zn = models.FloatField('Zn, мкг/л', default=0)
    cu = models.FloatField('Cu, мкг/л', default=0)
    mo = models.FloatField('Mo, мкг/л', default=0)
    co = models.FloatField('Co, мкг/л', default=0)
    si = models.FloatField('Si, мкг/л', default=0)

    def __str__(self):
        return self.name
    

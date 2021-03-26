from django.db import models
from django.contrib.auth.models import User
from datetime import *
# Create your models here.


 #recursiva para configurar menus

class MenuItem(models.Model):   
    codigo = models.CharField(max_length=6)
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=200)
    url = models.CharField(max_length=100, default="javascript:void(0)")
    onclick = models.CharField(max_length=100,blank=True,default=" ")
    parent = models.ForeignKey('self',blank=True, null=True)   
    ruta_foto = models.ImageField(upload_to='menu_items/', null=True)

    class Meta:        
        db_table = 'menuapp_menu_item'
        ordering = ['codigo']
    
    def __unicode__(self):
        return "%s - %s"  % ( self.codigo,self.nombre)
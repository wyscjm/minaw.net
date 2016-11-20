#-*- coding: utf-8 -*-

from django.db                import models
#from .                        import fields
from django.core.urlresolvers import reverse


class MainModel(models.Model):
    added = models.DateTimeField (auto_now_add=True, verbose_name="Ajouté")
    modif = models.DateTimeField (auto_now=True    , verbose_name="Modifié")

    class Meta:
        abstract = True


class Module(MainModel):
    content      = models.TextField      (blank=True, verbose_name="contenu")
    semester     = models.ForeignKey     ('Semester', verbose_name="semestre")
    subject      = models.ForeignKey     ('Subject',  verbose_name="matière")
    teacher      = models.ForeignKey     ('Teacher',  verbose_name="enseignant")

    def __unicode__(self):
        return self.semester.short + ' - ' + self.subject.short + ' - ' + self.teacher.short

    def get_absolute_url(self):
        return reverse('module', kwargs={'semester': self.semester.slug, 'subject': self.subject.slug, 'teacher':self.teacher.slug})

    class Meta:
        verbose_name = "module"
        ordering = ['semester', 'subject', 'teacher']


class Semester(MainModel):
    name  = models.CharField(max_length=16, verbose_name="nom")
    short = models.CharField(max_length=4,  verbose_name="nom abrégé")
    slug  = models.SlugField(               verbose_name="slug")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "semestre"


class Subject(MainModel):
    name  = models.CharField(max_length=32, verbose_name="nom")
    short = models.CharField(max_length=16, verbose_name="nom abrégé")
    slug  = models.SlugField(               verbose_name="slug")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "matière"


class Teacher(MainModel):
    name  = models.CharField(max_length=32, verbose_name="nom")
    short = models.CharField(max_length=16, verbose_name="nom abrégé")
    slug  = models.SlugField(               verbose_name="slug")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "enseignant"
        ordering = ['slug']


class Comment(MainModel):
    module    = models.ForeignKey               ('Module', related_name='comments',             verbose_name="module")
    content   = models.TextField                (                                               verbose_name="contenu")
    author    = models.CharField                (max_length=32,                  default='',    verbose_name="auteur")
    validated = models.BooleanField             (                                default=False, verbose_name="validé")
    year      = models.PositiveSmallIntegerField(                                default=2016,  verbose_name="année") #TODO ranged YearField implementation

    def __unicode__(self):
        return str(self.module) + ' - ' + str(self.id)

    class Meta:
        verbose_name        = "avis"
        verbose_name_plural = "avis"

#coding:utf-8
from django.contrib import admin
from models import Article, Tag, Comment
# Register your models here.
from django.contrib import admin
from pagedown.widgets import AdminPagedownWidget
from django import forms
# Register your models here.

class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget= AdminPagedownWidget())
	class Meta:
		model = Article
		fields = '__all__'
class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm

admin.site.register(Article,ArticleAdmin)

admin.site.register(Tag)
admin.site.register(Comment)



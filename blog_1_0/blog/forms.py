# -*- coding: utf-8 -*-
# @Time    : 17-3-16 下午3.16
# @Author  : lzz
# @Site    : blog
# @File    : forms.py
# @Software: PyCharm

from django.contrib.auth.models import User
from django import forms

class CommentForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(required= False)
    content = forms.CharField()

class AuthorForm(forms.ModelForm):
    # 错误信息
    error_messages = {
        'duplicate_username': u"此用户已存在.",
        'password_mismatch': u"两次密码不相等.",
        'duplicate_email': u'此email已经存在.'
    }
    username = forms.CharField(
        max_length=15,
        error_messages={
            'invalid': '用户名无效,15字符以内',
            'required': '用户名未填'
        }
    )
    email = forms.EmailField(
        error_messages={
            'invalid': '邮件格式错误，参考1xx@163.com',
            'required': 'email未填'
        }
    )
    passwd = forms.CharField(
        widget= forms.PasswordInput,
        error_messages={
            'required': '密码未填'
        }
    )
    re_passwd = forms.CharField(
        widget= forms.PasswordInput,
        error_messages={
            'required': '请再输一次密码'
        }
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User._default_manager.get(username= username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_re_passwd(self):
        passwd = self.cleaned_data.get("passwd")
        re_passwd = self.cleaned_data.get("re_passwd")
        if passwd and re_passwd and re_passwd != passwd:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"]
            )
        return re_passwd

    def save(self, commit=True):
        user = super(AuthorForm, self).save(commit= False)
        user.set_password(self.cleaned_data["passwd"])
        if commit:
            user.save()
        return user
from django import forms

# 类名随意
class UserForm(forms.Form):
    username = forms.CharField(max_length=8,label='姓名',required=True)
    password = forms.CharField(max_length=8,min_length=6,label='密码')

    # 固定写法
    def clean_username(self):
        # 校验数据
        # 获取数据
        username = self.cleaned_data.get('username')
        # 校验规则
        if 'admin' in username:
            # 校验不通过
            self.add_error('username','用户名不能包含admin')
        else:
            # 校验通过
            return username
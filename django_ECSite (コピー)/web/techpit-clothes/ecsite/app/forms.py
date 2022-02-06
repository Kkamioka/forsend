from django import forms
from .models import line_items

# 出勤用
class CreateForm(forms.ModelForm):

    class Meta:
        model = line_items
        # 今回は保存値がすでに決まっているのでfield,widgetsは不要
        # 必要ならばここに追加
        fields = (
        )
        widgets = {
        }


from django import forms
import re
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class LinkForm(forms.Form):
    link = forms.CharField(widget=forms.Textarea(attrs={'cols': 85, 'rows': 1}), required=True)

    # def clean(self):
    #     data = self.cleaned_data['link']
    #     second_part = data.split("v=")[1].split("&ab")[0]
    #     first_part = data.split(second_part)[0]
    #     third_part = data.split(second_part)[1]
    #     if re.match("https://www.youtube.com/watch", first_part):
    #         if re.match("[A-Za-z0-9]", second_part):
    #             if "&ab_channel=" in third_part:
    #                 return data
    #             else:
    #                 raise ValidationError("錯誤的網址")
    #         else:
    #             raise ValidationError("錯誤的網址")
    #
    #     else:
    #         raise ValidationError("錯誤的網址")


#"https://www.youtube.com/watch?v=HMJiX77z4AU&t=851s&ab_channel=ITZY"
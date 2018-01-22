from django import template

register = template.Library()

dictionary = {'old_password': 'Old Password',
              'new_password1': 'New Password',
              'new_password2': 'Repeat Password',
              'username': 'Username',
              'password': 'Password',
              'email': 'Email Address'
              }


@register.filter(name='addcss')
def addcss(field, css):
    print(field.field.widget.__class__)
    return field.as_widget(attrs={"class": css, "placeholder": checker(field.html_name)})


def checker(field_html_name):
    if field_html_name in dictionary:
        return dictionary[field_html_name]
    else:
        return field_html_name

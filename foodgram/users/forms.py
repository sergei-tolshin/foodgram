from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(label=_("Email"), max_length=254, required=True)
    password2 = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')

    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

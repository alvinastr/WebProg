from django import forms
from account.models import AccountUser


class StudentRegisterForm(forms.Form):
    fullname = forms.CharField(
        label='Nama Lengkap', label_suffix=" : ", required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'John Smith'}),
        help_text="Nama lengkap mahasiswa", error_messages={'required': "Harus Diisi"})
    nim = forms.CharField(
        label='Nim', label_suffix=" : ", required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '102988444'}),
        help_text="nomor induk mahasiswa", error_messages={'required': "Harus Diisi"})
    email = forms.CharField(
        label='email', label_suffix=" : ", required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'john@smith.co'}),
        help_text="email aktif", error_messages={'required': "Harus Diisi"})

    class Meta:
        model = AccountUser
        fields = ('account_user_fullname','account_user_student_number', 'email')

    def clean(self):
        super(StudentRegisterForm, self).clean()

        fullname = self.cleaned_data.get("fullname")
        if not fullname: self._errors['fullname'] = self.error_class(['Harus di isi!'])

        nim = self.cleaned_data.get("nim")
        if not nim: self._errors['nim'] = self.error_class(['Harus di isi!'])

        email = self.cleaned_data.get("email")
        if not email: self._errors['email'] = self.error_class(['Harus di isi!'])
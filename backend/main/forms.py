from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, 
                          widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'required': "OTP is required",
                          'max_length': "OTP must be exactly 6 digits"
                          })
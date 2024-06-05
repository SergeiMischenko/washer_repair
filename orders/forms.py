from django import forms

from orders.models import RepairRequest


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ["name", "surname", "phone", "email", "model_washer", "description"]


class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ["name", "surname", "phone"]

from django import forms

from orders.models import RepairRequest, Review


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ["name", "surname", "phone", "email", "model_washer", "description"]


class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ["name", "surname", "phone"]


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["order", "text", "rating"]
        widgets = {
            "order": forms.HiddenInput(),
        }

from django import forms

from accounts.models import AerpawUser
from experiments.models import Experiment
from .models import Reservation
from resources.models import Resource
from resources.resources import is_resource_available_time

class ReservationCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.experiment_id = kwargs.pop('experiment_id')
        super(ReservationCreateForm,self).__init__(*args,**kwargs)

    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
        label='Reservation Name',
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Resource Description',
    )
    
    resource = forms.ModelChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=True,
        widget=forms.Select(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Reservation
        fields = (
            'name',
            'description',
            'resource',
            'units',
            'start_date',
            'end_date',
        )
    
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        qs=Experiment.objects.filter(id=self.experiment_id)
        if not qs.exists():
            return redirect("/")
        experiment=qs.first()
        stage=experiment.stage

        rs=cleaned_data.get("resource")
        qs=Resource.objects.filter(name=rs)
        if not qs.exists():
            return redirect("/")
        resource=qs.first()

        if not resource.is_correct_stage(stage):
            raise forms.ValidationError("This resource is not in yourexperiment's stage!")

        start_date=cleaned_data.get("start_date")
        end_date=cleaned_data.get("end_date")
        is_available = is_resource_available_time(resource,start_date, end_date)
        if not is_available:
            raise forms.ValidationError("This resource has no units avaialble for reservation at this time!")

        return cleaned_data

class ReservationChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'size': 60}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        required=False,
        label='Reservation Description',
    )

    resource = forms.ModelChoiceField(
        queryset=Resource.objects.order_by('name'),
        required=False,
        widget=forms.Select(),
        label='Resource',
    )

    units = forms.IntegerField(
        required=True,
        initial=0,
        widget=forms.NumberInput(),
        label='Resource Units',
    )

    class Meta:
        model = Reservation
        fields = (
            'name',
            'description',
            'resource',
            'units',
            'start_date',
            'end_date',
        )

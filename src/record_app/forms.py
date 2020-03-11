from .models import RecordData
from django import forms



class RecordModelForm(forms.ModelForm):
	class Meta:
		model = RecordData
		fields = [
			'equipmentID',
			'equipmentDesc',
			'building',
			'elevation',
			'roomID',
			'notes',
		]
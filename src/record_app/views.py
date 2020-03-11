import csv, io
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from .models import RecordData
from .forms import RecordModelForm

# Create your views here.

def record_app_create_page(request):
	
	
	# prompt = {
	# "Order" : "order of csv should be"
	# }
	# csv_file = request.FILES['file']
	# if not csv_file.name.endswith('.csv'):
	# 	messages.error(request, 'Thisis not a csv file')

	# data_set = csv_file.read().decode('UTF-8')
	# io_string = io.StringIO(data_set)
	# next(io_string)
	# for column in csv.reader(io_string, delimiter=',', quotechar="|"):
	# 	_, created = RecordData.objects.update_or_create(

	# 		'equipmentID', = column[0],
	# 		'equipmentDesc', = 
	# 		'building', = 
	# 		'elevation', = 
	# 		'roomID', = 
	# 		'notes', = 
	# 		)

	form = RecordModelForm(request.POST or None)
	if form.is_valid():
		# print(form.cleaned_data)
		# obj = RecordData.objects.create(**form.cleaned_data)
		# obj.save()
		form.save()
		form = RecordModelForm()
	# context = {"object":obj}
	template_name = 'record_app_create_view.html'
	return render(request, template_name)



def record_app_table_page(request):
	# obj = RecordData.objects.get(id=id)
	# obj = get_object_or_404(RecordData,id=id)
	obj = RecordData.objects.all()
	template_name = 'record_app_table_view.html'
	context = {"object":obj}
	return render(request, template_name, context)

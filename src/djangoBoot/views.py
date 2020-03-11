from django.shortcuts import render
# from record_app.models import RecordData


def home_page(request):

	template_name = 'index3.html'
	return render(request, template_name, {})



from django.shortcuts import render
from django.http import HttpResponse
from .models import Face
from .forms import FaceForm


def index(request):
    face = Face.objects.all()

    if request.method == 'GET':
        return render(request, 'index.html', {'prov': 'Yeeees', 'face': face, 'form': FaceForm()})

    if request.method == 'POST':
        print(request.FILES)
        form = FaceForm(request.POST, request.FILES)
        if form.is_valid():
            face_id = form.cleaned_data.get('face_id')
            name = form.cleaned_data.get("face_name")
            img = form.cleaned_data.get("face_img")
            obj = Face.objects.create(
                face_id=face_id,
                face_img=img,
                face_name=name
            )
            obj.save()
            print(obj)
            return  render(request, 'index.html', {'prov': 'Yeeees', 'face': face,'form':FaceForm()})


    context ={}
    context['form']= FaceForm()
    return render(request, 'index.html', {'prov': request, 'face': face,'form':FaceForm()})


# def added(request):
#     # if request.method == "POST" and request.POST:
#     # try:
#     #         face_id = request.POST['face_id']
#     #        print('ok')
#     #       face_name = request.POST['face_name']
#     #      print('ok')
#     #     face_img = request.FILES['face_img']
#     #    print('ok')
#     #   created_obj = Face.objects.create(face_id=face_id, face_name=face_name, face_img=face_img)
#     #  print('ok')
#     # created_obj.save()
#     # except Exception as e:
#     #   return HttpResponse(e)
#
#     # context = {}
#     # if request.method == "POST":
#     #     form = FaceForm(request.POST)
#     #     # if form.is_valid():
#     #     print('form is valid')
#     #     face_name = request.POST.get("face_name")
#     #     face_img = request.POST.get("face_id")
#     #     face_id = request.FILES['face_img']
#     #     created_obj = Face.objects.create(face_id=face_id, face_name=face_name, face_img=face_img)
#     #     print('ok')
#     #     created_obj.save()
#     #     print(created_obj)
#     #     # else:
#     #     # form = FaceForm()
#     #     context['form'] = form
#
#     if request.method == 'POST':
#         print(request.FILES)
#         form = FaceForm(request.POST, request.FILES)
#         if form.is_valid():
#             face_id = form.cleaned_data.get('face_id')
#             name = form.cleaned_data.get("face_name")
#             img = form.cleaned_data.get("face_img")
#             obj = Face.objects.create(
#                 face_id=face_id,
#                 face_img=img,
#                 face_name=name
#             )
#             obj.save()
#             print(obj)
#             return HttpResponse('OK')
#
#
#     #return HttpResponse('mmmmmm')

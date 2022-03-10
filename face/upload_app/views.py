from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Face
from .forms import FaceFormRegister
import cryptocode

def auth(request):
    if request.method == 'POST':
        face_token_ch = request.POST['password']
        if Face.objects.filter(face_token_ch=face_token_ch).exists():
            return redirect('index')
        return render(request,'auth.html',{'prov': 'Blyat'})
    return render(request, 'auth.html',{'prov': 'Blyt2'})



def index(request):
    face = Face.objects.all()

    if request.method == 'GET':
        try:
            data = {
                'face_id_ch': request.GET['face_id_ch'],
                'face_name_ch': request.GET['face_name_ch']
            }
        except :
            data = {}
        return render(request, 'index.html', {'prov': request, 'face': face, 'form': FaceFormRegister(data)})

    if request.method == 'POST':
        try:
            print(request.FILES)
            form = FaceFormRegister(request.POST, request.FILES)
            if form.is_valid():
                face_id = form.cleaned_data.get('face_id_ch')
                name = form.cleaned_data.get("face_name_ch")
                img = form.cleaned_data.get("face_img")
                token = form.cleaned_data.get('face_token_int')
                token_valid = 'True'
                group = form.cleaned_data.get('face_group_ch')
                worker = form.cleaned_data.get('face_worker_bol')
                obj = Face.objects.create(
                    face_id_ch=face_id,
                    face_name_ch=name,
                    face_img=img,
                    face_token_int=token,
                    face_token_valid_bol=token_valid,
                    face_group_ch=group,
                    face_worker_bol=worker
                )
                obj.save()
                print(obj)
                return  render(request, 'index.html', {'prov': 'Yeeees', 'face': face,'form':FaceFormRegister()})
        except Exception as e:
            render(request, 'index.html', {'prov': 'Oshibka', 'face': face, 'form': FaceFormRegister()})


    return render(request, 'index.html', {'prov': 'request', 'face': face,'form':FaceFormRegister()})


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

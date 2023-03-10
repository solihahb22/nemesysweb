from django.core.files.uploadedfile import UploadedFile

def load_parameter_optb(file:UploadedFile):
    for line in file.chunks():
        str = line.decode('utf-8')
        print(str)
from . import models
from PIL import Image
from django.shortcuts import get_object_or_404


def image_filename(pk):
    user = get_object_or_404(models.Profile, pk=pk)
    image = str(user.avatar)
    img_list = image.split('/')
    filename = img_list[-1]
    return filename



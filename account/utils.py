import os
from uuid import uuid4

from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from PIL import Image


class OverwriteStorage(FileSystemStorage):
    """ Overwrite the file when upload a file with the same name
    """

    def get_available_name(self, name, max_length=None):
        """ Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


@deconstructible
class UploadToPathAndRename(object):
    """ Rename the uploaded file name
    """

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)


def create_avatar(file_path):
    """ Create avartar from the picture uploaded
    """

    size = 256, 256

    img = Image.open(file_path)
    img.thumbnail(size, Image.ANTIALIAS)

    avatar = Image.new(mode='RGBA', size=size, color=(255,255,255,0))
    avatar.paste(img, (max((size[0] - img.size[0]) / 2, 0),
        max((size[1] - img.size[1]) / 2, 0)))
    avatar.save(file_path,'PNG')

    return True
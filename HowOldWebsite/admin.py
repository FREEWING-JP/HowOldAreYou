# -*- coding: UTF-8 -*-

from django.contrib import admin

from .models import RecordOriginalImage
from .models import RecordFace
from .models import RecordSex
from .models import RecordAge
from .models import RecordSmile
from .models import ModelSex
from .models import ModelAge
from .models import ModelSmile

admin.site.register(RecordOriginalImage)
admin.site.register(RecordFace)
admin.site.register(RecordSex)
admin.site.register(RecordAge)
admin.site.register(RecordSmile)
admin.site.register(ModelSex)
admin.site.register(ModelAge)
admin.site.register(ModelSmile)

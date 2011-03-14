# -*- coding: utf-8 -*-

import os, sys
try:
    from pytils.translit import slugify
except ImportError:
    slugify = None


def ext_slugify(value, model, instance):
    slug = slugify(value)
    count = model.objects.filter(slug=slug).count()
    if count == 1 and model.objects.get(slug=slug) == instance:
        return slug
    if count > 0:
        i = 2
        while 1:
            newslug = slug + "_%d" % i
            if model.objects.filter(slug=newslug).count() == 0:
                return newslug
            i += 1
    return slug



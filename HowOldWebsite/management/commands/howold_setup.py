# -*- coding: UTF-8 -*-

import os

import django.conf
from django.core.management.base import BaseCommand

__author__ = 'Hao Yu'


class Command(BaseCommand):
    help = 'Setup the HowOldAreYou website.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("We are installing the HowOldAreYou website on your server.")

        print("Making directories...")
        for directory in django.conf.settings.SAVE_DIR:
            directory = directory.strip()
            if not os.path.exists(directory):
                os.makedirs(directory)

        print("Success! Have fun!")

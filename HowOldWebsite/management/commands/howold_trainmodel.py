# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand

from HowOldWebsite.trainers.util_trainer import UtilTrainer

__author__ = 'Hao Yu'


class Command(BaseCommand):
    help = 'Train models.'

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='+')

    def handle(self, *args, **options):
        train_models = []
        model_names = ['sex', 'age', 'smile']
        for m in options['models']:
            if m in model_names:
                train_models.append(m)

        print("=" * 10 + " We are training model(s) {}" + '=' * 10)
        print("The following model(s) will be trained:", end=" ")
        for m in train_models:
            print(m, end=" ")
        print()

        success = UtilTrainer.train(train_models)

        # print("=" * 10 + " Train model success " + '=' * 10)

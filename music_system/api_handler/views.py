from django.shortcuts import render
from django.http import HttpResponse


# Here we will create all ouur endpoints


def main(request):
    return HttpResponse("<h1>Hello</h1>")


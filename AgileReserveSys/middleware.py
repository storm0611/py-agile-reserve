from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class ActivateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # do something before the request is handled by the view
        pass
            

    def process_response(self, request, response):
        # do something after the response is generated by the view
        return response
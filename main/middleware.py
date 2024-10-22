from django.http import HttpResponsePermanentRedirect

class RedirectToCustomDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is coming from the Azure domain
        if request.get_host().endswith('azurewebsites.net'):
            # Redirect to the custom domain (www.uwsil.com)
            return HttpResponsePermanentRedirect(f'https://www.uwsil.com{request.path}')

        response = self.get_response(request)
        return response

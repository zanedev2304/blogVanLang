from django.shortcuts import redirect






class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.path == '/login/':
            return redirect('account_profile')
        
        return response



class MicrosoftUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.session.get('user')
        request.microsoft_user = user
        print(user)  # Kiểm tra thông tin user trong terminal
        response = self.get_response(request)
        return response

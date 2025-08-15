

class StoreUserRoleMiddleware:
    # store variable 'rolel' in sessions
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        role = request.GET.get('role')
        if role in ['driver', 'passenger']:
            request.session['role'] = role
        response = self.get_response(request)
        return response

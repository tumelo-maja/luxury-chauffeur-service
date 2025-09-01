"""
Custom middleware for the `users` app.
"""


class StoreUserRoleMiddleware:
    """
    Middleware to store the user's role in the session when signing up.

    Attributes
    ----------
    get_response : callable
        The next view in within the request session.

    Methods
    -------
    __call__(request)
        Stores the 'role' argument, passed with the request, in the session.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request before passing it further.

        Gets the 'role' query parameter and stored in the session.

        Returns
        -------
        HttpResponse
            The response object passed to
                the next view with `role` in its session.
        """
        role = request.GET.get('role')
        if role in ['driver', 'passenger']:
            request.session['role'] = role
        response = self.get_response(request)
        return response

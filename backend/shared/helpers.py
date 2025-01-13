from . import error


def get_user_business(user):
    """
    Helper function to retrieve the business associated with the owner.
    Returns a tuple (business, error_response), where one is None.
    """
    business = getattr(user.owner, 'business', None)

    if not business:
        error_response = error.builder(404, 'Owner does not have a business.')
        return None, error_response
    
    return business, None

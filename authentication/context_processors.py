
def user_context(request):
    """Context processor to add user information to all templates"""
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            return {
                'user_display_name': request.user.first_name or request.user.username,
                'user_profile_picture': profile.get_profile_picture,
                'user_position': profile.position
            }
        except:
            return {
                'user_display_name': request.user.username,
                'user_profile_picture': 'https://i.imgur.com/UkrjXEc.jpg',
                'user_position': 'Church Administrator'
            }
    return {}

from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.models import User
from computers.models import Brand

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            profile_photo_url = profile.profile_photo.url if profile.profile_photo else static('images/default-profile.png')
        except User.profile.RelatedObjectDoesNotExist:
            profile_photo_url = static('images/user.png')
        return {
            'profile_photo_url': profile_photo_url
        }
    return {}

def allBrands(request):
    brands = Brand.objects.all()
    return {'brands':brands}

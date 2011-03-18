import settings
def theme(request):
    return {"theme" : settings.MEDIA_URL + request.session.get("theme", "lollerz")}

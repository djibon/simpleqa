from badge.models import UserBadgeMessage

def badge_messages(request):
    if request.user.is_authenticated():
        badge_messages = UserBadgeMessage.objects.filter(userbadge__user=request.user,display=False)
        for bm in badge_messages:
            bm.display=True
            bm.save()
        return {
            'badge_messages':badge_messages
            }
    return {}

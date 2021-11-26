from memo.models import Profile, Goal, Question, Theme, Section


def profile_exists(user):
    return Profile.objects.filter(user=user).exists()


def create_profile(user):
    return Profile.objects.create(user=user)


def get_goals_by_profile(profile):
    return profile.goals.all()

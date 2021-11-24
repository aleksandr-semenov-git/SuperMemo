from rest_framework import serializers
from memo.models import Profile, Goal, Question, Theme, Section


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user']
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='user_images/%Y/%m/%d', default='user_images/default.jpg')


class GoalSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=50, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='goals', on_delete=models.CASCADE,
                                null=True)

    def __str__(self):
        return self.name


class SectionSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=50, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='sections', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ThemeSerializer(serializers.ModelSerializer):
    name = models.CharField(max_length=200, db_index=True, null=True)
    section = models.ForeignKey(Section, verbose_name='section', related_name='themes', on_delete=models.CASCADE, null=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='themes', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class LessonSerializer(serializers.ModelSerializer):
    name = models.IntegerField(default=1)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='lessons',  on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, verbose_name='profile', related_name='lessons',  on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)


class QuestionSerializer(serializers.ModelSerializer):
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=500, null=True)
    lesson = models.ForeignKey(Lesson, verbose_name='lesson', related_name='questions', on_delete=models.CASCADE,
                               null=True)
    theme = models.ForeignKey(Theme, verbose_name='theme', related_name='questions', on_delete=models.CASCADE,
                              null=True)
    section = models.ForeignKey(Section, verbose_name='section', related_name='questions', on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, verbose_name='goal', related_name='questions', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question
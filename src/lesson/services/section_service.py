from django.db.models import Q
from django.shortcuts import get_object_or_404
from lesson.models import Section
from memo.models import Goal


class SectionService:
    @staticmethod
    def get_section_by_id(section_id: int) -> Section:
        return get_object_or_404(Section, pk=section_id)

    @staticmethod
    def get_section_by_name_and_goal_id(name, goal_id) -> Section:
        return get_object_or_404(Section, Q(name=name), Q(goal__id=goal_id))

    @staticmethod
    def create_section(name: str, goal: Goal) -> Section:
        return Section.objects.create(name=name, goal=goal)
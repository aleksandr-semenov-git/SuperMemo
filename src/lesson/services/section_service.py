from django.db.models import Q
from django.shortcuts import get_object_or_404
from lesson.models import Section
from memo.models import Goal


class SectionService:
    @staticmethod
    def get_section_by_id(section_id: int) -> Section:
        """Take section_id, return section or raise Http404 exception"""
        return get_object_or_404(Section, pk=section_id)

    @staticmethod
    def get_section_by_name_and_goal_id(name: str, goal_id: int) -> Section:
        """Take name and goal_id, return section or raise Http404 exception"""
        return get_object_or_404(Section, Q(name=name), Q(goal__id=goal_id))

    @staticmethod
    def create_section(name: str, goal: Goal) -> Section:
        """Take name and goal, return created section"""
        return Section.objects.create(name=name, goal=goal)

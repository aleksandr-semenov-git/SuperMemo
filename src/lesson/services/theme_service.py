from django.db.models import Q
from django.shortcuts import get_object_or_404
from lesson.models import Section, Theme


class ThemeService:
    @staticmethod
    def get_theme_by_id(theme_id: id) -> Theme:
        """Take theme_id, return theme or raise Http404 exception"""
        return get_object_or_404(Theme, pk=theme_id)

    @staticmethod
    def get_theme_by_name_and_section_id(name: str, section_id: int) -> Theme:
        """Take name and section_id, return theme or raise Http404 exception"""
        return get_object_or_404(Theme, Q(name=name), Q(section__id=section_id))

    @staticmethod
    def create_theme(name: str, section: Section) -> Theme:
        """Take name and section, return create theme"""
        return Theme.objects.create(name=name, section=section)

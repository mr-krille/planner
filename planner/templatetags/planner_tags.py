from datetime import date

from django import template

register = template.Library()


@register.filter
def grid_start(assignment, days):
    """
    Calculates the 1-based CSS Grid starting column for an assignment.
    Finds the first visible day that falls within the assignment's date range.
    """
    for i, day in enumerate(days):
        if assignment.start_date <= day <= assignment.end_date:
            return i + 1  # CSS Grid columns are 1-indexed
    return 1


@register.filter
def grid_span(assignment, days):
    """
    Calculates how many grid columns (visible days) the assignment spans.
    Counts intersection of the assignment dates with the 10-day view window.
    Because our grid omits weekends, this perfectly handles tasks spanning over the weekend!
    """
    count = 0
    for day in days:
        if assignment.start_date <= day <= assignment.end_date:
            count += 1
    return count

def get_date_diff_display(start, end):
    if end.year != start.year:
        return '%s - %s' % (start.strftime('%-d %b %Y'), end.strftime('%-d %b %Y'))

    # year are same now
    if end.month != start.month:
        return '%s - %s, %s' % (start.strftime('%-d %b'), end.strftime('%-d %b'), start.year)

    # month and year are same now
    if end.day != start.day:
        return '%s-%s %s, %s' % (start.strftime('%d'), end.strftime('%d'), start.strftime('%b'), start.year)

    # day, month and year are same now
    if end.strftime('%p') != start.strftime('%p'):
        return '%s - %s, %s' % (start.strftime('%-I:%M%p'), end.strftime('%-I:%M%p'), start.strftime('%-d %b %Y'))

    # am/pm, day, month and year are same now
    return '%s - %s%s' % (start.strftime('%-I:%M'), end.strftime('%-I:%M'), start.strftime('%p, %-d %b %Y'))

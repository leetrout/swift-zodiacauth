from bisect import bisect

# bisect pattern
# http://stackoverflow.com/questions/3274597/how-would-i-determine-zodiac-astro
# logical-star-sign-from-a-birthday-in-python
# dates
# http://en.wikipedia.org/wiki/Zodiac#Table_of_dates
ZODIAC_DATES_SIGNS = [
    (1, 20, "capricorn"),
    (2, 19, "aquarius"),
    (3, 20, "pisces"),
    (4, 19, "aries"),
    (5, 20, "taurus"),
    (6, 20, "gemini"),
    (7, 21, "cancer"),
    (8, 22, "leo"),
    (9, 22, "virgo"),
    (10, 22, "libra"),
    (11, 21, "scorpio"),
    (12, 21, "sagittarius"),
    (12, 31, "capricorn")
]


def zodiac_sign(mon, day):
    """
    Returns the string representation of a zodiac sign for the provided
    month and day.

    Month and day are both 1 based.

    >>> zodiac_sign(1, 1)
    'capricorn'
    >>> zodiac_sign(3, 14)
    'pisces'
    """
    return ZODIAC_DATES_SIGNS[bisect(ZODIAC_DATES_SIGNS, (mon, day))][2]


def zodiac_sign_datetime(dt_inst):
    """
    Returns the string representation of a zodiac sign for the provided
    datetime instance.

    >>> import datetime
    >>> dt = datetime.datetime(2011, 3, 14)
    >>> zodiac_sign_datetime(dt)
    'pisces'
    """
    return zodiac_sign(dt_inst.month, dt_inst.day)


def zodiac_acl_from_json(jsn_obj):
    """
    Converts the given ACL from an object directly representing the ACL
    as described in the JSON file to one that is more efficient for look ups.

    >>> jsn = [[u'aries', u'aries', [u'0.0.0.0']]]
    >>> zodiac_acl_from_json(jsn)
    {u'aries': {u'aries': [u'0.0.0.0']}}
    """
    acl = {}
    # for each entry in the list
    for store_sign, access_sign, ips_list in jsn_obj:
        store_sign = store_sign.lower()
        access_sign = access_sign.lower()
        acl[store_sign] = {access_sign: ips_list}
    return acl

from datetime import datetime, timezone, timedelta
import time

# Converts UTC datetime to local time using the system's local timezone, considering DST
def utc_to_local(utc_dt):
    if utc_dt is None:
        return None  # Handle None values
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)  # Make it UTC if it's naive

    # Get local time offset (difference from UTC), taking DST into account
    local_offset = timedelta(seconds=-time.timezone) if time.localtime().tm_isdst == 0 else timedelta(seconds=-time.altzone)
    
    # Apply local timezone offset
    local_timezone = timezone(local_offset)
    return utc_dt.astimezone(local_timezone)

# Custom datetime formatting with timezone abbreviation
def format_datetime(dt, format='%m/%d/%Y %I:%M:%S %p'):
    """Converts UTC datetime to local time and formats it with a timezone abbreviation."""
    if dt is None:
        return "Not available"
    
    local_dt = utc_to_local(dt)
    
    # Use strftime to format the datetime, adding the timezone abbreviation manually
    timezone_abbr = get_timezone_abbreviation(local_dt)
    
    return local_dt.strftime(f"{format} {timezone_abbr}")

def get_timezone_abbreviation(dt):
    """Returns the timezone abbreviation (e.g., CST, CDT, EST, etc.) considering DST."""
    # Check if the datetime is in daylight saving time or standard time
    if dt.dst() != timedelta(0):  # DST is in effect
        # Timezone abbreviations (DST)
        if -18000 <= dt.utcoffset().total_seconds() <= -14400:  # UTC-5 (Eastern Time DST)
            return "EDT"
        elif -21600 <= dt.utcoffset().total_seconds() <= -18000:  # UTC-6 (Central Time DST)
            return "CDT"
        elif -25200 <= dt.utcoffset().total_seconds() <= -21600:  # UTC-7 (Mountain Time DST)
            return "MDT"
        elif -28800 <= dt.utcoffset().total_seconds() <= -25200:  # UTC-8 (Pacific Time DST)
            return "PDT"
    else:  # Standard Time
        # Timezone abbreviations (Standard Time)
        if -18000 <= dt.utcoffset().total_seconds() <= -14400:  # UTC-5 (Eastern Time)
            return "EST"
        elif -21600 <= dt.utcoffset().total_seconds() <= -18000:  # UTC-6 (Central Time)
            return "CST"
        elif -25200 <= dt.utcoffset().total_seconds() <= -21600:  # UTC-7 (Mountain Time)
            return "MST"
        elif -28800 <= dt.utcoffset().total_seconds() <= -25200:  # UTC-8 (Pacific Time)
            return "PST"
    
    # Default case: use the built-in timezone abbreviation
    return dt.strftime("%Z")

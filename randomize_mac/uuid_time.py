from datetime import datetime, timezone
import uuid

'''
# The standard library uses an approach without datetime:
import calendar
import time
def uuid_now(epoch = (1582, 10, 15, 0, 0, 0, 2, 283, -1)):
    """100-ns intervals since 1582-10-15 00:00:00 in the morning, on a Wednesday
    epoch = -0x01b21dd213814000 is that value

    This is currently a 57-bit number
    """
    if isinstance(epoch, tuple):
        epoch = calendar.timegm(epoch)
    return int((time.time()-epoch)*1E7)

# for timezone awareness:
def uuid_now(epoch=datetime(1582, 10, 15, tzinfo=timezone.utc)):
    """100-ns intervals since 1582-10-15 00:00:00 in the morning, on a Wednesday
    """
    return int((datetime.now(tz=timezone.utc)-epoch).total_seconds()*1E7)
'''

def uuid_now(epoch=datetime(1582, 10, 15)):
    """100-ns intervals since 1582-10-15 00:00:00 in the morning, on a Wednesday
    """
    return int((datetime.now()-epoch).total_seconds()*1E7)

def uuid_date_and_time(now=uuid_now()):
    m = int(1E7)*60*60*24
    d, t = divmod(now, m)
    return d*m, t

def uuid_today(*args, **kwargs):
    m, _ = uuid_date_and_time(*args, **kwargs)
    return m

def replace_timestamp(u, now=uuid_today()):
    """The UUID timestamp is set to the latest midnight.
    """
    clock_seq_hi_variant, clock_seq_low, node = u.fields[3:6]
    time_low = now & 0xffffffff
    time_mid = (now >> 32) & 0xffff
    time_hi_version = (now >> 48) & 0x0fff
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version, \
        clock_seq_hi_variant, clock_seq_low, node), version=1)

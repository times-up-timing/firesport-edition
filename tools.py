def ms_to_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds,100)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "Time: {:02d}:{:02d}:{:02d}".format(minutes, seconds,milliseconds)
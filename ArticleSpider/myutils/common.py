import re



# 获取文本中的数字
from datetime import datetime


def extract_num(text):

    match_re = re.match('.*?(\d+).*', text[0])
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums
def int2date(intger):
    dateArray=datetime.utcfromtimestamp(intger)
    return dateArray.strftime("%Y-%m-d")
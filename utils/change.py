def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def change_name(value):
    if value == "server_category":
        value = "서버문의"
    elif value == "support_category":
        value = "후원문의"
    elif value == "report_category":
        value = "신고하기"
    elif value == "log_channel":
        value = "로그채널"

    return value

def change_type(value):
    if value == "log_channel":
        value = "채널"
    else:
        value = "카테고리"
    
    return value

def AM_PM(value):
    am_pm = value
    if am_pm == "AM":
        am_pm = "오전"
    elif am_pm == "PM":
        am_pm = "오후"

    return am_pm
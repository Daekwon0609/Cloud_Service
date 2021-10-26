def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def change_name(value):
    replace_value = {"server_category": "서버문의", "support_category": "후원문의", "report_category": "신고하기", "log_channel": "로그채널"}
    value = replace_all(value, replace_value)

    return value

def change_type(value):
    replace_value = {"log_channel": "채널", "server_category": "카테고리", "support_category": "카테고리", "report_category": "카테고리"}
    value = replace_all(value, replace_value)
    
    return value

def AM_PM(value):
    replace_value = {"AM": "오전", "PM": "오후"}
    am_pm = replace_all(value, replace_value)

    return am_pm
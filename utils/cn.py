def change_name(value):
    if value == "server_category":
        value = "서버문의"
    elif value == "support_category":
        value = "후원문의"
    elif value == "report_category":
        value = "신고하기"

    return value
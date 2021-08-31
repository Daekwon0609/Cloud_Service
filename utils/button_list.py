from discord_slash.utils.manage_components import create_button, create_actionrow

from discord_slash.model import ButtonStyle

service_buttons_1 = create_actionrow(
    create_button(
        style=ButtonStyle.green,
        label="서버문의",
        custom_id="server_category"
    ),
    create_button(
        style=ButtonStyle.blue,
        label="후원문의",
        custom_id="support_category"
    ),
    create_button(
        style=ButtonStyle.red,
        label="신고하기",
        custom_id="report_category"
    ),
    create_button(
        style=ButtonStyle.gray,
        label="취소하기",
        custom_id="service_queue_cancel"
    )
)

scr_bt = create_actionrow(
    create_button(
        style=ButtonStyle.red,
        label="종료하기",
        custom_id="close"
    ),
    create_button(
        style=ButtonStyle.blue,
        label="이동하기",
        custom_id="move"
    )
)

cancel_bt = create_actionrow(
    create_button(
        style=ButtonStyle.red,
        label="취소하기",
        custom_id="cancel"
    )
)
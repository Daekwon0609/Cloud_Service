from interactions.utils.manage_components import create_button, create_actionrow, create_select, create_select_option

from interactions.model import ButtonStyle

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

create_select_value = create_actionrow(
    create_select(
        options=[
            create_select_option(
                label="서버문의",
                value="server_category"
            ),
            create_select_option(
                label="후원문의",
                value="support_category"
            ),
            create_select_option(
                label="신고하기",
                value="report_category"
            )
        ],
        placeholder="생성할 카테고리 종류를 선택해 주세요",
        min_values=1,
        max_values=1,
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

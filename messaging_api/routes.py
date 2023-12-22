from fastapi.routing import APIRoute

from messaging_api import endpoints, schemas

AUTH_HEADER_REMINDER_TEXT = (
    '<br>The authentication headers `username` and `password` are required."'
)

app_routes = (
    APIRoute(
        "/users/", response_model=schemas.User,
        endpoint=endpoints.user_create, methods=["POST"],
        name="create_new_user",
        description=(
            'Create a new user using `username` and `password`.<br>'
            'Field `id` is optional.'
        )
    ),
    APIRoute(
        "/users/", response_model=list[schemas.User], methods=["GET"],
        endpoint=endpoints.user_list, name="users_list",
        description=(
            'Get list of all existing users. `skip` and `limit` can be used '
            f'for limit/offset pagination. {AUTH_HEADER_REMINDER_TEXT}'
        )
    ),
    APIRoute(
        "/users/{user_id}/messages/", response_model=schemas.Message,
        endpoint=endpoints.user_message_create, methods=["POST"],
        name="create_message_from_user",
        description=(
            'Create a new message from user.\n'
            '* User has to exist.\n'
            '* Creating messages on behalf of other users is not allowed.'
            f'{AUTH_HEADER_REMINDER_TEXT}'
        )
    ),
    APIRoute(
        "/messages/", response_model=list[schemas.Message],
        endpoint=endpoints.user_message_list, methods=["GET"],
        name="messages_list",
        description=(
            'Get list of all existing messages by user ID or from all of '
            f'them, if user_id is not provided.{AUTH_HEADER_REMINDER_TEXT}'
        )
    )
)

#!/usr/bin/python3


# MatrixAmnesia is a simple script for removing user messages from Matrix room
#     Copyright (C) 2026  Kirill Shakirov
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import argparse

import nio
from nio import AsyncClient, LoginResponse, RoomRedactError, RoomMessagesResponse


async def main(server:str, user_id:str, password:str, room_id:str, del_interval: int):

    # Create an async client
    client = AsyncClient(server, user_id)

    # Log in
    print("Logging in...")
    response = await client.login(password)

    if isinstance(response, LoginResponse):
        print("Logged in successfully.")
    else:
        print(f"Login failed: {response}")
        await client.close()
        return 1

    my_messages = set()
    start_token = None
    for i_count in range(100000):
        # get next messages chunk
        resp = await client.room_messages(
            room_id=room_id,
            start=start_token,
            limit=1000,
            message_filter={"senders": [user_id], "types": ["m.room.message"]})

        if isinstance(resp, nio.RoomMessagesError):
            print(f"Error! Failed to get messages: {resp}")
            await client.close()
            return 1

        if isinstance(resp, RoomMessagesResponse):
            for event in resp.chunk:
                if isinstance(event, nio.RoomMessage):
                    my_messages.add(event.event_id)

            start_token = resp.end
            if start_token is None:
                break

    print(f"Total messages to delete: {len(my_messages)}")

    del_count = 0
    failed_count = 0
    for event_id in my_messages:
        await asyncio.sleep(del_interval)
        res = await client.room_redact(room_id=room_id, event_id=event_id, reason="redacted")
        if isinstance(res, RoomRedactError):
            print(f"Deleting message_id:{event_id} - Failed!")
            failed_count += 1
        else:
            print(f"Deleting message_id:{event_id} - OK!")
            del_count += 1

    print(f"Total messages: {len(my_messages)}")
    print(f"Deleted: {del_count}")

    await client.close()
    return 0


if __name__ == '__main__':
    # Initialize arguments parser
    parser = argparse.ArgumentParser(
        prog="matrix_amnesia.py",
        description="This program finds all messages in Matrix room and sends redact requests for them.",
        epilog="Have a nice day!",
        color=True)

    parser.add_argument("-s", "--server",
                        action="store",
                        default=None,
                        help="homeserver, for example \"https://matrix.org\"",
                        required=True)

    parser.add_argument("-u", "--user",
                        action="store",
                        default=None,
                        help="user id, for example \"@user:matrix.org\"",
                        required=True)

    parser.add_argument("-p", "--password",
                        action="store",
                        default=None,
                        help="user password",
                        required=True)

    parser.add_argument("-r", "--room",
                        action="store",
                        default=None,
                        help="room ID from which to delete messages",
                        required=True)

    parser.add_argument("-i", "--interval",
                        action="store",
                        type=int,
                        default=5,
                        help="interval in seconds between redaction requests",
                        required=False)


    arguments = parser.parse_args()
    asyncio.run(main(server=arguments.server,
                     user_id=arguments.user,
                     password=arguments.password,
                     room_id=arguments.room,
                     del_interval=arguments.interval))


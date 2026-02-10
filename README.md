## MatrixAmnesia
MatrixAmnesia is a simple script for removing user messages from Matrix room

It intended for user who wants to delete his messages from a chatroom.
So script makes list of message ids from user, and then sends "redact" request for each message with specified timeout (so server won't ban or kik user).

Server receiving this request should clear message content.

I wanted to clean my messages from one chat room, but was unable to find the way to do it...
So, I made this script.

It depends on matrix-nio python lib.

```commandline
usage: matrix_amnesia.py [-h] -s SERVER -u USER -p PASSWORD -r ROOM [-i INTERVAL]

This program finds all messages in Matrix room and sends redact requests for them.

options:
  -h, --help                 show this help message and exit
  -s, --server SERVER        homeserver, for example 'https://matrix.org'
  -u, --user USER            user id, for example '@user:matrix.org'
  -p, --password PASSWORD    user password
  -r, --room ROOM            room ID from which to delete messages
  -i, --interval INTERVAL    interval in seconds between redaction requests
```



*This program is free software: you can redistribute it and/or modify*
*it under the terms of the GNU General Public License as published by*
*the Free Software Foundation, either version 3 of the License, or*
*(at your option) any later version.*

*This program is distributed in the hope that it will be useful,*
*but WITHOUT ANY WARRANTY; without even the implied warranty of*
*MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the*
*GNU General Public License for more details.*

*You should have received a copy of the GNU General Public License*
*along with this program.  If not, see <https://www.gnu.org/licenses/>.*


Copyright (C) 2026  Kirill Shakirov
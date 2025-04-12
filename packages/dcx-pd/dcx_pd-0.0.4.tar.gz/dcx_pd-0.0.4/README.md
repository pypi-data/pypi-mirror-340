# dcx-pd
_[**D**iscord **C**hat E**x**porter](https://github.com/Tyrrrz/DiscordChatExporter) (by [Tyrrrz](https://github.com/Tyrrrz)) json output parser to typed **P**y**d**antic V2 objects_

**NOTE**: This project has no affiliation with Discord nor Tyrrrz. This was made by another person and is unofficial.

# Installation
`$ pipx install dcx-pd` (pipx, recommended)
or
`$ pip install dcx-pd`

## How to use:
After installation `dcx` entry point will be available in your shell.

<details><summary> Linux and Mac </summary>


Provide list of paths to json files as arguments (space separated):
```bash
$ dcx /exports/* # automatically expand the glob via bash/zsh/unix shells
# OR
$ dcx /exports/server1-channel1-1234123412341234.json /exports/server1-channel2-507642999992352779.json
```

</details>

<details><summary> Windows </summary>

Provide list of paths to json files as arguments (space separated):
```cmd
> dcx /exports/server1-channel1-1234123412341234.json /exports/server1-channel2-507642999992352779.json
```

</details>

You will be put in an interactive python interpreter, with pre-set variables `export` and `exports`. There's also a better `sys.displayhook` which will color the output of any object you inspect.
```
==> Loading 'server1-channel1-1234123412341234.json'...
==> Loading 'server1-channel2-507642999992352779.json'...
==> Loaded 10,250 messages (mem: 176.70MB)
==> (i) Variables export and exports contain exports[0] and the list[dcx.Export] itself respectively
==> Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
>>>
```
You can use any python expression to filter through the exports. Filtering mechanisms may be added in future versions, example:

```py
>>> [message for export in exports for message in export.messages if "hello" in message.content].__len__()
4
>>> [message for export in exports for message in export.messages if "hello" in message.content]
[
Message(**{
        "id": 1234123412341234,
        "type": MessageType.REPLY: "Reply",
        "timestamp": <21:47:04.838000+0200 27-04-2024, Sat>,
        "timestamp_edited": None,
        "timestamp_call_ended": None,
        "is_pinned": False,
        "content": "uhhh hello? downloadmoreram.com",
        "author": {
            "color": 0xAA00FF,
            "id": 1234123412341234,
            "name": "example",
            "discriminator": "0000",
            "nickname": "Example",
            "is_bot": False,
            "avatar_url": "/exports/assets/avatar0.png",
            "roles": [],
        },
        "attachments": [],
        "embeds": [],
        "stickers": [],
        "reactions": [],
        "mentions": [],
        "inline_emojis": None,
        "reference": {
            "message_id": 123123123123123123,
            "channel_id": 12345123451234512345,
            "guild_id": 1234561234561234561234,
        },
        "interaction": None,
    }),
]
```

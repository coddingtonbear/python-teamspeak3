# Teamspeak3 API

This python module allows you to interact with an instance of Teamspeak running
on your computer using Python rather than using the built-in lua interface.

## Use

I wrote this library to satisfy a need on my part, so you can find a detailed
example at https://bitbucket.org/latestrevision/teamspeak-notification, but
briefly, let's go over subscribing to incoming messages the hard way:

    import teamspeak3

    client = teamspeak3.Client()
    client.send_command(
        teamspeak3.Command(
            'clientnotifyregister', {
                'event': 'any',
                'schandlerid': '0'
            }
        )
    )

    while True:
        messages = client.get_messages()
        for message in messages:
            if message.command == 'notifytextmessage':
                print message

in the above, you can see how you first create the client instance, and then
send to teamspeak a command object asking that it register for incoming
notifications-- I have written a shortcut for subscriptions, too, so the above
can be simplified to:

    import teamspeak3

    client = teamspeak3.Client()
    client.subscribe()

    while True:
        messages = client.get_messages()
        for message in messages:
            if message.command == 'notifytextmessage':
                print message

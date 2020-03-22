class Error(Exception):
    pass


class MessageError(Error):
    pass


class MessageDatabase:
    def __init__(self):
        self.discord_messages = []
        self.messages_info = []

    def get_message(self, author=None, content=None, message_id=None, time=None):
        for message in self.discord_messages:
            if message.id == message_id:
                return message

        for message in self.messages_info:
            if message.get("time") == time:
                return message

        for message in self.messages_info:
            if message.get("content") == content:
                return message

        for message in self.messages_info:
            if message.get("author") == author:
                return message

        raise MessageError("Can't identify Message by given arguments.")

    def add_message(self, message_object, time):
        self.discord_messages.append(message_object)
        self.messages_info.append(
            {
                "content": message_object.content,
                "author": message_object.author,
                "time": round(time)
            }
        )

    def del_message(self, author=None, content=None, message_id=None, time=None):
        for message in self.discord_messages:
            if message.id == message_id:
                self.discord_messages.pop(self.discord_messages.index(message))
                self.messages_info.pop(self.messages_info.index(message))
                return True

        for message in self.messages_info:
            if message.get("time") == time:
                self.discord_messages.pop(self.discord_messages.index(message))
                self.messages_info.pop(self.messages_info.index(message))
                return True

        for message in self.messages_info:
            if message.get("content") == content:
                self.discord_messages.pop(self.discord_messages.index(message))
                self.messages_info.pop(self.messages_info.index(message))
                return True

        for message in self.messages_info:
            if message.get("author") == author:
                self.discord_messages.pop(self.discord_messages.index(message))
                self.messages_info.pop(self.messages_info.index(message))
                return True

        return False

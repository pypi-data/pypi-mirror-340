from .core import SafeW
#Messaging def
def sendMessage(self, chat_id, text, **kwargs):
    data = {"chat_id": chat_id, "text": text, **kwargs}
    return self.request("sendMessage", data)

def editMessageText(self, chat_id, message_id, text, **kwargs):
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, **kwargs}
    return self.request("editMessageText", data)

def editMessageCaption(self, chat_id, message_id, caption, **kwargs):
    data = {"chat_id": chat_id, "message_id": message_id, "caption": caption, **kwargs}
    return self.request("editMessageCaption", data)

def deleteMessage(self, chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    return self.request("deleteMessage", data)

def forwardMessage(self, chat_id, from_chat_id, message_id):
    data = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id}
    return self.request("forwardMessage", data)

def copyMessage(self, chat_id, from_chat_id, message_id, **kwargs):
    data = {"chat_id": chat_id, "from_chat_id": from_chat_id, "message_id": message_id, **kwargs}
    return self.request("copyMessage", data)

def pinChatMessage(self, chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    return self.request("pinChatMessage", data)

def unpinChatMessage(self, chat_id, message_id=None):
    data = {"chat_id": chat_id}
    if message_id:
        data["message_id"] = message_id
    return self.request("unpinChatMessage", data)

SafeW.send_message = sendMessage
SafeW.edit_message_text = editMessageText
SafeW.edit_message_caption = editMessageCaption
SafeW.delete_message = deleteMessage
SafeW.forward_message = forwardMessage
SafeW.copy_message = copyMessage
SafeW.pin_message = pinChatMessage
SafeW.unpin_message = unpinChatMessage
#This linking the SafeW core with messages defers.
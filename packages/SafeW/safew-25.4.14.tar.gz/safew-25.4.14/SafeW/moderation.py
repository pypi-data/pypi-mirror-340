from .core import SafeW
#Moderations 
def banChatMember(self, chat_id, user_id):
    data = {"chat_id": chat_id, "user_id": user_id}
    return self.request("banChatMember", data)

def restrictChatMember(self, chat_id, user_id, permissions):
    data = {"chat_id": chat_id, "user_id": user_id, "permissions": permissions}
    return self.request("restrictChatMember", data)

def promoteChatMember(self, chat_id, user_id, **kwargs):
    data = {"chat_id": chat_id, "user_id": user_id, **kwargs}
    return self.request("promoteChatMember", data)

def getChat(self, chat_id):
    data = {"chat_id": chat_id}
    return self.request("getChat", data)

def getChatAdministrators(self, chat_id):
    data = {"chat_id": chat_id}
    return self.request("getChatAdministrators", data)

def getChatMember(self, chat_id, user_id):
    data = {"chat_id": chat_id, "user_id": user_id}
    return self.request("getChatMember", data)

def leaveChat(self, chat_id):
    data = {"chat_id": chat_id}
    return self.request("leaveChat", data)

SafeW.ban_chat_member = banChatMember
SafeW.restrict_chat_member = restrictChatMember
SafeW.promote_chat_member = promoteChatMember
SafeW.get_chat = getChat
SafeW.get_chat_administrators = getChatAdministrators
SafeW.get_chat_member = getChatMember
SafeW.leave_chat = leaveChat
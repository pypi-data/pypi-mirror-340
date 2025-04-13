from .core import SafeW
#Media Controlling
def sendPhoto(self, chat_id, photo, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"photo": photo}
    return self.request("sendPhoto", data, files)

def sendVideo(self, chat_id, video, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"video": video}
    return self.request("sendVideo", data, files)

def sendDocument(self, chat_id, document, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"document": document}
    return self.request("sendDocument", data, files)

def sendAudio(self, chat_id, audio, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"audio": audio}
    return self.request("sendAudio", data, files)

def sendVoice(self, chat_id, voice, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"voice": voice}
    return self.request("sendVoice", data, files)

def sendAnimation(self, chat_id, animation, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"animation": animation}
    return self.request("sendAnimation", data, files)

def sendSticker(self, chat_id, sticker, **kwargs):
    data = {"chat_id": chat_id, **kwargs}
    files = {"sticker": sticker}
    return self.request("sendSticker", data, files)

SafeW.send_photo = sendPhoto
SafeW.send_video = sendVideo
SafeW.send_document = sendDocument
SafeW.send_audio = sendAudio
SafeW.send_voice = sendVoice
SafeW.send_animation = sendAnimation
SafeW.send_sticker = sendSticker
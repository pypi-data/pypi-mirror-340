#SafeW(25.4.12)
**Arabic & English documentation below**

<p align="center">
  <img src="https://static.pepy.tech/badge/ftpsocket" height="30" />
  <img src="https://static.pepy.tech/badge/ftpsocket/month" height="30" />
</p>

---
##
version=`25.4.14`
## التنصيب | Installation

```bash
pip install safew==25.4.14
```

---

## الاستخدام السريع | Quick Usage

### العربية
```python
from safew import SafeW
bot = SafeW("YOUR_BOT_TOKEN")
bot.send_message(chat_id=123456789, text="أهلا بك!")
```

### English
```python
from safew import SafeW
bot = SafeW("YOUR_BOT_TOKEN")
bot.send_message(chat_id=123456789, text="Welcome!")
```

---

## الميزات | Features

- إرسال رسائل | Send messages: `sendMessage`
- إرسال صور، فيديو، مستندات | Media sending: `sendPhoto`, `sendVideo`, `sendDocument`
- حذف الرسائل | Delete messages: `deleteMessage`
- معلومات البوت | Bot info: `getMe`
- الحظر | Ban: `banChatMember`
- الردود التفاعلية | Inline/Callback responses: `answerInlineQuery`, `answerCallbackQuery`
- دعم خيارات | Option support: `reply_markup`, `parse_mode`, `protect_content`

---
---

## المساهمة | Contributing

المكتبة مفتوحة المصدر وتقبل المساهمات.
The `library` is open-source and welcomes contributions.

from .core import SafeW
#InlineAnswering.
def answerInlineQuery(self, inline_query_id, results, **kwargs):
    data = {"inline_query_id": inline_query_id, "results": results, **kwargs}
    return self.request("answerInlineQuery", data)

def answerCallbackQuery(self, callback_query_id, **kwargs):
    data = {"callback_query_id": callback_query_id, **kwargs}
    return self.request("answerCallbackQuery", data)

SafeW.answer_inline_query = answerInlineQuery
SafeW.answer_callback_query = answerCallbackQuery
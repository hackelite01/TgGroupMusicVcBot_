from pyrogram.handlers import InlineQueryHandler
from youtubesearchpython import VideosSearch
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from pyrogram import Client, errors
from helpers import wrap
from strings import _


@Client.on_inline_query()
@wrap
def search(client, query):
    answers = []
    string = query.query.lower().strip().rstrip()

    if string == "":
        client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=_("inline_1"),
            switch_pm_parameter="help",
            cache_time=0
        )
        return
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=_("inline_2").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=_("inline_3"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]

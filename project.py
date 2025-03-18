from simple_blogger import CommonBlogger
from simple_blogger.generators.YandexGenerator import YandexTextGenerator
from simple_blogger.generators.YandexGenerator import YandexImageGenerator
from datetime import datetime
from datetime import timedelta
from simple_blogger.senders.TelegramSender import TelegramSender

class Project(CommonBlogger):
    def _example_task_creator(self):
        return [
            {
                "book": "book",
                "author": "author"
            }
        ]

    def _get_category_folder(self, task):
        return f"{task['author']}"
                    
    def _get_topic_folder(self, task):
        return f"{task['book']}"

    def _system_prompt(self, _):
        return f"Ты - школьный блоггер, книгоман, прочитавший более 1000 книг, используешь в разговоре сленг {self.age}-летних подростков и смайлики"

    def _task_converter(self, idea):
        return { 
                    "author": idea['author'],
                    "book": idea['book'],
                    "topic_prompt": f"Расскажи {self.age}-летнему подростку без спойлеров, почему стоит прочитать книгу '{idea['book']}' автора {idea['author']}, используй не более {self.topic_word_limit} слов",
                    "topic_image": f"Нарисуй картинку, вдохновлённую книгой '{idea['book']}' автора {idea['author']}, крупный план, глубина, гиперреализм",
                }

    def __init__(self, age=12, **kwargs):
        #from simple_blogger.generators.OpenAIGenerator import OpenAITextGenerator
        super().__init__(
            first_post_date=datetime(2025, 6, 9),
            text_generator=YandexTextGenerator(model_version='rc'),
            image_generator=YandexImageGenerator(),
            topic_word_limit=150,
            days_between_posts=timedelta(days=2),
            reviewer=TelegramSender(),
            senders=[TelegramSender(channel_id=f"@class5nik")],
            **kwargs
        )
        self.age = age

    def gen_all(self):
        import json
        import time
        tasks = json.load(open(self.tasks_file, "rt", encoding="UTF-8"))
        for task in tasks:
            self.gen_text(task=task)
            #self.gen_image(task=task)
            time.sleep(1)



    
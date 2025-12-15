import os
import json
import logging
import pytesseract
import pynput

from src.TelegramBot import TelegramBot
from src.ImageClass import ImageClass
from src.LogClass import LogClass

class Core:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, "data", "config.json")

        self.config: dict = None
        self.telegrambot: TelegramBot = None

        self.question = ImageClass()
        self.answer = ImageClass()
        self.log_file = LogClass()

        self.text = None


    def load(self):
        self.load_config(self.config_path)

        self.kb_listener = pynput.keyboard.GlobalHotKeys({
            'u': lambda rect=self.question: self.take_rect(rect),
            'i': lambda rect=self.answer: self.take_rect(rect),
            'h': self.create_query,
            'd': self.send,
            'z': self.check,
            'g': self.get,
            'n': self.stop
        })
        pytesseract.pytesseract.tesseract_cmd = os.path.join(self.base_dir, "Tesseract-OCR", "tesseract.exe")

        self.telegrambot = TelegramBot(self.config["token"], self.config["chat_id"])

        if self.config["coords_question"]:
            self.question.coords = tuple(self.config["coords_question"])
            self.log.info(self.question.coords)
        if self.config["coords_answer"]:
            self.answer.coords = tuple(self.config["coords_answer"])

    def load_config(self, file):
        self.logger("starting load config")

        with open(file, "r") as json_file:
            self.config = json.load(json_file)

    def save_config(self, file):
        self.logger("starting save config")

        with open(file, "w") as json_file:
            json.dump(self.config, json_file)

    def run(self):
        self.logger("Starting")

        self.kb_listener.start()
        # LAST!!!!!
        self.telegrambot.start()


    def stop(self):
        self.logger("Closing")

        if self.question.coords:
            self.config["coords_question"] = self.question.coords
        if self.answer.coords:
            self.config["coords_answer"] = self.answer.coords
        self.config["chat_id"] = self.telegrambot.get_last_user_id()
        self.save_config(self.config_path)

        self.log_file.stop()
        self.kb_listener.stop()
        self.telegrambot.stop()

        os._exit(0)

    def send(self):
        self.logger("Sending send")
        self.telegrambot.send_text(self.text)
        self.logger("Ending send")

    def check(self):
        self.logger("Checking user")
        self.telegrambot.send_text("U're here?")
        self.logger("Stop check user")

    def get(self):
        result = self.telegrambot.get_text()
        self.logger(f"r {result}")

    def take_rect(self, rect):
        self.logger("finding image")
        rect.find()
        self.logger("ending image")

    def create_query(self):
        if not self.question.coords and not self.answer.coords:
            self.log.info("No have image")
            return

        self.logger("Take screenshot")

        self.question.take_screenshot()
        self.answer.take_screenshot()

        self.logger("Starting create query")

        self.question.save_image(os.path.join(self.base_dir, "data", "question.png"))
        self.answer.save_image(os.path.join(self.base_dir, "data", "answer.png"))

        question = pytesseract.image_to_string(self.question.image, lang="eng+rus")
        answer = pytesseract.image_to_string(self.answer.image, lang="eng+rus")

        question = " ".join(question.split())
        answer = " ".join(answer.split())

        self.text = f"{question} \n \n {answer}"

        self.logger("Ending_create_query")

    def logger(self, msg: str):
        self.log_file.rename(msg)
        self.log.info(msg)

import os
import json
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class RussianFactsAPI:
    """Класс для получения русскоязычных фактов из различных источников"""

    @staticmethod
    def get_random_fact() -> str:
        """Возвращает случайный интересный факт на русском"""
        facts = [
            "Мозг человека на 60% состоит из жира.",
            "В Японии есть специальные звукопоглощающие столбы, чтобы заглушить шум от поездов.",
            "Сердце креветки находится в ее голове.",
            "Кошки могут издавать более 100 различных звуков, а собаки только около 10.",
            "В Швейцарии запрещено мыть машину по воскресеньям.",
            "Мед никогда не портится. Археологи находили съедобный мед в гробницах фараонов.",
            "У осьминога три сердца.",
            "В Исландии нет комаров.",
            "Человек моргает примерно 15-20 раз в минуту, то есть около 12 миллионов раз в год.",
            "Язык жирафа может достигать длины 45 см.",
            "Свет от Солнца до Земли доходит за 8 минут 20 секунд.",
            "В Древнем Риме моча использовалась как чистящее средство для одежды.",
            "Пингвины могут прыгать в высоту до 2 метров.",
            "В России находится самое глубокое озеро в мире - Байкал.",
            "Ленивцы спускаются с деревьев только раз в неделю, чтобы сходить в туалет.",
            "У улитки около 25 000 зубов.",
            "Финляндия - самая счастливая страна в мире (по данным World Happiness Report).",
            "Человеческое тело содержит достаточно железа, чтобы сделать гвоздь длиной 7,5 см.",
            "В Японии больше всего в мире торговых автоматов - около 5 миллионов.",
            "Земля - единственная планета, не названная в честь бога."
        ]
        return random.choice(facts)

    @staticmethod
    def get_topics() -> List[str]:
        """Возвращает список доступных тем"""
        return ["животные", "наука", "география", "история", "технологии", "культура", "спорт", "кухня", "здоровье"]

    @staticmethod
    def get_fact_by_topic(topic: str) -> Optional[str]:
        """Возвращает случайный факт по заданной теме"""
        topic_facts = {
            "животные": [
                "У осьминога три сердца.",
                "Сердце креветки находится в ее голове.",
                "Кошки проводят около 70% своей жизни во сне.",
                "Улитки могут спать до 3 лет.",
                "Язык жирафа может достигать длины 45 см.",
                "Пингвины могут прыгать в высоту до 2 метров.",
                "Ленивцы спускаются с деревьев только раз в неделю.",
                "У улитки около 25 000 зубов.",
                "Колибри - единственная птица, которая умеет летать назад.",
                "Слоны могут учуять воду на расстоянии до 5 км."
            ],
            "наука": [
                "Мозг человека на 60% состоит из жира.",
                "Свет от Солнца до Земли доходит за 8 минут 20 секунд.",
                "Человек моргает примерно 15-20 раз в минуту.",
                "В человеческом теле около 37 триллионов клеток.",
                "Кости человека в 4 раза прочнее бетона.",
                "Земля вращается со скоростью около 1670 км/ч на экваторе.",
                "Атомы на 99,9999999999999% состоят из пустого пространства.",
                "У человека и банана около 50% общих генов.",
                "Венера - единственная планета, вращающаяся против часовой стрелки.",
                "Один год на Венере длится 225 земных дней."
            ],
            "география": [
                "В России находится самое глубокое озеро в мире - Байкал.",
                "В Исландии нет комаров.",
                "Финляндия - самая счастливая страна в мире.",
                "В Японии больше всего в мире торговых автоматов.",
                "Канада имеет самую длинную береговую линию в мире.",
                "В Сибири находится 25% мировых лесов.",
                "Россия - самая большая страна в мире по площади.",
                "В Чили находится самая сухая пустыня в мире - Атакама.",
                "В Австралии больше кенгуру, чем людей.",
                "В Гренландии самое большое количество айсбергов."
            ],
            "история": [
                "В Древнем Риме моча использовалась как чистящее средство.",
                "Наполеон был атакован кроликами во время охоты.",
                "Викинги использовали птиц для навигации в море.",
                "В Древнем Египте фараоны носили накладные бороды.",
                "Первые ножницы были изобретены в Древнем Риме.",
                "В Средневековье пиво было безопаснее воды.",
                "Древние греки использовали камни вместо туалетной бумаги.",
                "В XIX веке кетчуп продавался как лекарство.",
                "Клеопатра жила ближе к изобретению iPhone, чем к строительству пирамид.",
                "В Древнем Китае использовали бумажные деньги уже в VII веке."
            ],
            "технологии": [
                "Первый компьютерный вирус был создан в 1983 году.",
                "Пароль '123456' до сих пор один из самых популярных.",
                "Первая компьютерная мышь была сделана из дерева.",
                "Самый первый сайт в интернете до сих пор работает.",
                "Первая камера на телефоне появилась в 2000 году.",
                "Wi-Fi был изобретен в 1991 году.",
                "Первое SMS было отправлено в 1992 году.",
                "YouTube был основан тремя бывшими сотрудниками PayPal.",
                "Первая игра в истории - 'Tennis for Two' (1958).",
                "Самый первый домен в интернете - symbolics.com."
            ],
            "культура": [
                "В Швейцарии запрещено мыть машину по воскресеньям.",
                "В Японии есть специальные звукопоглощающие столбы.",
                "В Саудовской Аравии нет кинотеатров до 2018 года.",
                "Во Франции запрещено называть свинью Наполеоном.",
                "В Сингапуре запрещено жевать жвачку.",
                "В Италии больше объектов Всемирного наследия ЮНЕСКО, чем в любой другой стране.",
                "В Индии больше всего в мире вегетарианцев.",
                "В Бразилии говорят на португальском, а не на испанском.",
                "В Канаде самый высокий уровень образования в мире.",
                "В Японии самая высокая продолжительность жизни."
            ],
            "спорт": [
                "Футбол - самый популярный вид спорта в мире.",
                "Баскетбол был изобретен в 1891 году в США.",
                "Волейбол был изобретен в 1895 году.",
                "Хоккей с шайбой появился в Канаде в XIX веке.",
                "Теннис зародился во Франции в XII веке.",
                "Плавание было включено в Олимпийские игры в 1896 году.",
                "Бег на 100 метров - самая короткая дистанция в легкой атлетике.",
                "Шахматы - один из старейших видов спорта.",
                "Серфинг был изобретен в Полинезии 4000 лет назад.",
                "Скалолазание стало олимпийским видом спорта в 2020 году."
            ],
            "кухня": [
                "Мед никогда не портится.",
                "Помидор - это фрукт, а не овощ.",
                "Морковь изначально была фиолетовой.",
                "Кетчуп изначально был рыбным соусом.",
                "Шоколад был валютой у древних майя.",
                "Сыр был изобретен более 7000 лет назад.",
                "Чай - второй по популярности напиток после воды.",
                "Кофе был открыт в Эфиопии в IX веке.",
                "Соль когда-то ценилась на вес золота.",
                "Яблоки плавают, потому что на 25% состоят из воздуха."
            ],
            "здоровье": [
                "Смех укрепляет иммунную систему.",
                "Ходьба пешком продлевает жизнь.",
                "Сон укрепляет память.",
                "Вода составляет около 60% веса тела взрослого человека.",
                "Человек делает около 20 000 вдохов в день.",
                "Улыбка задействует 17 мышц лица.",
                "Человек теряет около 50-100 волос в день.",
                "Ногти на руках растут в 4 раза быстрее, чем на ногах.",
                "Сердце перекачивает около 7500 литров крови в день.",
                "Человек может прожить без воды около 3 дней."
            ]
        }

        if topic.lower() in topic_facts:
            return random.choice(topic_facts[topic.lower()])
        return None


class FactsDataManager:
    """Класс для управления данными фактов"""

    def __init__(self, data_file: str = "russian_facts.json"):
        self.data_file = data_file
        self.api = RussianFactsAPI()
        self.facts_data = self._load_facts_data()

    def _load_facts_data(self) -> Dict:
        """Загружает факты из файла или создает новый"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Создаем начальную структуру данных
                data = {}
                for topic in self.api.get_topics():
                    fact = self.api.get_fact_by_topic(topic)
                    if fact:
                        data[topic] = [fact]

                # Добавляем случайные факты
                data["случайные"] = [self.api.get_random_fact() for _ in range(10)]

                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return data

        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            return {"случайные": [self.api.get_random_fact()]}

    def get_topics(self) -> List[str]:
        """Возвращает список доступных тем"""
        topics = list(self.facts_data.keys())
        if "случайные" in topics:
            topics.remove("случайные")
        return topics

    def get_random_fact(self) -> str:
        """Возвращает случайный факт"""
        all_facts = []
        for topic_facts in self.facts_data.values():
            all_facts.extend(topic_facts)

        if all_facts:
            return random.choice(all_facts)
        return self.api.get_random_fact()

    def get_fact_by_topic(self, topic: str) -> Optional[str]:

        topic_lower = topic.lower()

        # Получаем факт напрямую из API (где большой список)
        fact = self.api.get_fact_by_topic(topic_lower)

        if fact:
            # Сохраняем факт в локальный файл, чтобы расширять базу (но не читаем её обратно)
            if topic_lower not in self.facts_data:
                self.facts_data[topic_lower] = []
            if fact not in self.facts_data[topic_lower]:
                self.facts_data[topic_lower].append(fact)
            self._save_data()
            return fact

        return None

    def _save_data(self):
        """Сохраняет данные в файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.facts_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Ошибка при сохранении данных: {e}")

    def add_fact(self, topic: str, fact: str) -> bool:
        """Добавляет новый факт в указанную тему"""
        try:
            topic_lower = topic.lower()

            if topic_lower not in self.facts_data:
                self.facts_data[topic_lower] = []

            self.facts_data[topic_lower].append(fact)
            self._save_data()
            logger.info(f"Добавлен новый факт в тему '{topic}'")
            return True

        except Exception as e:
            logger.error(f"Ошибка при добавлении факта: {e}")
            return False


class UserPreferences:
    """Класс для управления пользовательскими настройками"""

    def __init__(self, preferences_file: str = "user_preferences.json"):
        self.preferences_file = preferences_file
        self.preferences = self._load_preferences()

    def _load_preferences(self) -> Dict:
        """Загружает настройки пользователей из файла"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Ошибка при загрузке настроек: {e}")
            return {}

    def _save_preferences(self):
        """Сохраняет настройки пользователей в файл"""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"Ошибка при сохранении настроек: {e}")

    def get_user_preference(self, user_id: int, key: str, default=None):
        """Получает значение настройки пользователя"""
        user_id_str = str(user_id)
        if user_id_str in self.preferences:
            return self.preferences[user_id_str].get(key, default)
        return default

    def set_user_preference(self, user_id: int, key: str, value):
        """Устанавливает значение настройки пользователя"""
        user_id_str = str(user_id)
        if user_id_str not in self.preferences:
            self.preferences[user_id_str] = {}

        self.preferences[user_id_str][key] = value
        self._save_preferences()

    def get_favorite_topic(self, user_id: int) -> Optional[str]:
        """Получает любимую тему пользователя"""
        return self.get_user_preference(user_id, "favorite_topic")

    def set_favorite_topic(self, user_id: int, topic: Optional[str]):
        """Устанавливает любимую тему пользователя"""
        self.set_user_preference(user_id, "favorite_topic", topic)

    def get_user_stats(self, user_id: int) -> Dict:
        """Получает статистику пользователя"""
        stats = self.get_user_preference(user_id, "stats", {})
        return {
            "total_facts": stats.get("total_facts", 0),
            "last_active": stats.get("last_active", ""),
            "favorite_topic": self.get_favorite_topic(user_id)
        }

    def update_stats(self, user_id: int):
        """Обновляет статистику пользователя"""
        stats = self.get_user_preference(user_id, "stats", {})
        stats["total_facts"] = stats.get("total_facts", 0) + 1
        stats["last_active"] = datetime.now().isoformat()
        self.set_user_preference(user_id, "stats", stats)


class FactsBot:
    """Основной класс бота для интересных фактов"""

    def __init__(self, token: str):
        self.token = token
        self.data_manager = FactsDataManager()
        self.user_prefs = UserPreferences()

        # Инициализация приложения
        self.application = Application.builder().token(token).build()

        # Регистрация обработчиков
        self._setup_handlers()

    def _setup_handlers(self):
        """Настройка всех обработчиков команд и сообщений"""

        # Обработчики команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("random", self.random_fact_command))
        self.application.add_handler(CommandHandler("fact", self.fact_command))
        self.application.add_handler(CommandHandler("topics", self.topics_command))
        self.application.add_handler(CommandHandler("myfact", self.myfact_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        self.application.add_handler(CommandHandler("add", self.add_fact_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))

        # Обработчики callback-запросов (кнопки)
        self.application.add_handler(CallbackQueryHandler(self.button_handler))

        # Обработчик для кнопок клавиатуры
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_keyboard_input))

        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)

    def _create_topic_keyboard(self) -> InlineKeyboardMarkup:
        """Создает клавиатуру с темами"""
        topics = self.data_manager.get_topics()
        keyboard = []

        # Создаем кнопки по 2 в ряд
        for i in range(0, len(topics), 2):
            row = []
            for j in range(2):
                if i + j < len(topics):
                    topic = topics[i + j]
                    row.append(InlineKeyboardButton(
                        topic.capitalize(),
                        callback_data=f"topic_{topic}"
                    ))
            if row:
                keyboard.append(row)

        # Добавляем кнопку для случайного факта
        keyboard.append([InlineKeyboardButton("🎲 Случайный факт", callback_data="random")])

        return InlineKeyboardMarkup(keyboard)

    def _create_fact_keyboard(self, topic: str = None) -> InlineKeyboardMarkup:
        """Создает клавиатуру под фактом"""
        keyboard = []

        if topic and topic != "random":
            keyboard.append([
                InlineKeyboardButton("📚 Еще по этой теме", callback_data=f"topic_{topic}"),
                InlineKeyboardButton("⭐ В избранное", callback_data=f"fav_{topic}")
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("🎲 Случайный факт", callback_data="random"),
                InlineKeyboardButton("📚 Выбрать тему", callback_data="topics")
            ])

        keyboard.append([
            InlineKeyboardButton("📖 Все темы", callback_data="topics"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
        ])

        keyboard.append([
            InlineKeyboardButton("📝 Добавить факт", callback_data="add_fact"),
            InlineKeyboardButton("📊 Статистика", callback_data="stats")
        ])

        return InlineKeyboardMarkup(keyboard)

    def _create_main_keyboard(self) -> ReplyKeyboardMarkup:
        """Создает основную клавиатуру"""
        keyboard = [
            ["🎲 Случайный факт", "📚 Выбрать тему"],
            ["⭐ Мой факт", "📖 Все темы"],
            ["⚙️ Настройки", "📊 Статистика"],
            ["📝 Добавить факт", "❓ Помощь"]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    async def _safe_edit_message(self, query, text: str, reply_markup: Optional[InlineKeyboardMarkup] = None, parse_mode: Optional[str] = None):
        """
        Безопасно редактирует сообщение из callback_query.
        В случае ошибки (например, сообщение изменено/удалено) — отправляет новое сообщение в чат.
        """
        try:
            # Пытаемся отредактировать существующее сообщение
            await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except Exception as e:
            logger.warning(f"Не удалось отредактировать сообщение callback: {e}. Пытаюсь отправить новое сообщение.")
            try:
                # Если редактирование не удалось — отправляем новое сообщение в тот же чат
                if query.message and query.message.chat_id:
                    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
                else:
                    # как запасной вариант — отвечаем на callback
                    await query.answer(text, show_alert=False)
            except Exception as e2:
                logger.error(f"Не удалось отправить запасное сообщение: {e2}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user

        # Обновляем статистику
        if user and user.id:
            self.user_prefs.update_stats(user.id)

        welcome_message = (
            f"Привет, {user.first_name}! 👋\n\n"
            "Я бот, который рассказывает интересные факты!\n\n"
            "🎲 Получи случайный факт - нажми /random\n"
            "📚 Выбери тему - нажми /topics\n"
            "⭐ Факт по любимой теме - нажми /myfact\n\n"
            "Используй кнопки ниже или команды меню:"
        )

        reply_markup = self._create_fact_keyboard()

        # Некоторые версии telegram ожидают ParseMode, а строка 'Markdown' тоже работает
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = (
            "📋 Справка по командам:\n\n"
            "🎲 /random - Случайный интересный факт\n"
            "📚 /topics - Выбрать тему из списка\n"
            "📖 /fact [тема] - Факт по конкретной теме\n"
            "⭐ /myfact - Факт по вашей любимой теме\n"
            "⚙️ /settings - Настройки бота\n"
            "📝 /add - Добавить свой факт\n"
            "📊 /stats - Ваша статистика\n"
            "❓ /help - Эта справка\n\n"
            "Примеры:\n"
            "`/fact животные` - факт о животных\n"
            "`/add наука \"Новый факт\"` - добавить факт\n\n"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]))

    async def random_fact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /random - случайный факт"""
        user_id = update.effective_user.id if update.effective_user else None

        # Добавляем хранение последнего факта для пользователя
        if 'last_fact' not in context.user_data:
            context.user_data['last_fact'] = None

        # Получаем случайный факт
        fact = self.data_manager.get_random_fact()

        # Если факт совпадает с предыдущим, пробуем еще раз (максимум 3 попытки)
        attempts = 0
        while fact == context.user_data.get('last_fact') and attempts < 3:
            fact = self.data_manager.get_random_fact()
            attempts += 1

        # Сохраняем текущий факт
        context.user_data['last_fact'] = fact

        # Обновляем статистику
        if user_id:
            self.user_prefs.update_stats(user_id)

        # Создаем сообщение с кнопками
        message = f"🎲 Случайный факт:\n\n{fact}"
        reply_markup = self._create_fact_keyboard()

        # Отправляем или редактируем сообщение
        if update.callback_query:
            await self._safe_edit_message(
                query=update.callback_query,
                text=message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

    async def fact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /fact [тема]"""
        user_id = update.effective_user.id if update.effective_user else None

        if context.args:
            topic = ' '.join(context.args)
            fact = self.data_manager.get_fact_by_topic(topic)

            if fact:
                # Обновляем статистику
                if user_id:
                    self.user_prefs.update_stats(user_id)

                message = f"📖 Факт о {topic.capitalize()}:\n\n{fact}"
                reply_markup = self._create_fact_keyboard(topic)

                await update.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Тема '{topic}' не найдена.\n"
                    f"Используйте /topics чтобы увидеть все доступные темы."
                )
        else:
            await update.message.reply_text(
                "📖 Использование:\n"
                "`/fact [тема]`\n\n"
                "Пример:\n"
                "`/fact животные`\n"
                "`/fact наука`\n"
                "`/fact история`\n\n"
                "Или используйте /topics для выбора темы."
            )

    async def topics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /topics - показывает все темы"""
        topics = self.data_manager.get_topics()

        if topics:
            topics_list = "\n".join([f"• {topic.capitalize()}" for topic in topics])
            message = f"📚 Доступные темы:\n\n{topics_list}\n\nВыберите тему:"
            reply_markup = self._create_topic_keyboard()
        else:
            message = "⚠️ Темы пока не загружены. Попробуйте позже."
            reply_markup = None

        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def myfact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /myfact - факт по любимой теме"""
        user_id = update.effective_user.id
        favorite_topic = self.user_prefs.get_favorite_topic(user_id)

        if favorite_topic:
            fact = self.data_manager.get_fact_by_topic(favorite_topic)

            if fact:
                # Обновляем статистику
                self.user_prefs.update_stats(user_id)

                message = f"⭐Факт по вашей любимой теме ({favorite_topic.capitalize()}):\n\n{fact}"
                reply_markup = self._create_fact_keyboard(favorite_topic)

                await update.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Не удалось найти факты по теме '{favorite_topic}'.\n"
                    "Попробуйте выбрать другую любимую тему в настройках."
                )
        else:
            keyboard = [[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]]
            await update.message.reply_text(
                "⭐ У вас еще нет любимой темы!\n\n"
                "Чтобы установить любимую тему:\n"
                "1. Выберите тему через /topics\n"
                "2. Нажмите кнопку '⭐ В избранное'\n"
                "3. Или установите в /settings\n\n"
                "После этого вы сможете быстро получать факты по любимой теме!",
            'Markdown', reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /settings - настройки"""
        user_id = update.effective_user.id
        favorite_topic = self.user_prefs.get_favorite_topic(user_id)

        keyboard = [
            [InlineKeyboardButton("📚 Выбрать любимую тему", callback_data="set_favorite")],
            [InlineKeyboardButton("🗑️ Очистить избранное", callback_data="clear_favorite")],
            [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        if favorite_topic:
            message = f"⚙️ Настройки:\n\n⭐ Любимая тема: {favorite_topic.capitalize()}\n\nВыберите действие:"
        else:
            message = "⚙️ Настройки:\n\n⭐ Любимая тема: не установлена\n\nВыберите действие:"

        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def add_fact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /add - добавление факта"""
        if context.args and len(context.args) >= 2:
            try:
                topic = context.args[0].lower()
                fact_text = ' '.join(context.args[1:])

                # Проверяем длину
                if len(fact_text) < 10:
                    await update.message.reply_text("⚠️ Текст факта слишком короткий (минимум 10 символов).")
                    return

                if len(fact_text) > 500:
                    await update.message.reply_text("⚠️ Текст факта слишком длинный (максимум 500 символов).")
                    return

                # Добавляем факт
                success = self.data_manager.add_fact(topic, fact_text)

                if success:
                    await update.message.reply_text(
                        f"✅ Факт успешно добавлен в тему '{topic.capitalize()}'!\n\n"
                        f"📝 Ваш факт:\n{fact_text}\n\n"
                        f"Спасибо за вклад в нашу коллекцию! 🎉", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]])
                    )

                else:
                    await update.message.reply_text("❌ Не удалось добавить факт. Попробуйте позже.")

            except Exception as e:
                logger.error(f"Ошибка при добавлении факта: {e}")
                await update.message.reply_text("❌ Произошла ошибка. Проверьте формат команды.")
        else:
            await update.message.reply_text(
                "📝Добавление факта:\n\n"
                "Формат: `/add тема \"Текст факта\"`\n\n"
                "Пример:\n"
                "`/add животные \"Кошки могут поворачивать уши на 180 градусов\"`\n\n"
                "⚠️Требования:\n"
                "• Тема: одно слово (животные, наука и т.д.)\n"
                "• Текст: 10-500 символов\n"
                "• Факт должен быть интересным и правдивым!", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]])
            )

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /stats - статистика"""
        user_id = update.effective_user.id
        stats = self.user_prefs.get_user_stats(user_id)
        favorite_topic = stats.get("favorite_topic")

        message = (
            f"📊 Ваша статистика:\n\n"
            f"👤 Пользователь: {update.effective_user.first_name}\n"
            f"📖 Фактов просмотрено: {stats.get('total_facts', 0)}\n"
        )

        if favorite_topic:
            message += f"⭐ Любимая тема: {favorite_topic.capitalize()}\n"
        else:
            message += "⭐ Любимая тема: не установлена\n"

        if stats.get("last_active"):
            try:
                last_active = datetime.fromisoformat(stats["last_active"]).strftime("%d.%m.%Y %H:%M")
                message += f"🕐 Последняя активность: {last_active}\n"
            except Exception:
                message += f"🕐 Последняя активность: {stats.get('last_active')}\n"

        keyboard = [[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]]

        await update.message.reply_text(message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на инлайн-кнопки"""
        if not update.callback_query:
            return

        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        data = query.data

        try:
            if data == "random":
                # Случайный факт
                fact = self.data_manager.get_random_fact()
                self.user_prefs.update_stats(user_id)
                message = f"🎲 Случайный факт:\n\n{fact}"
                reply_markup = self._create_fact_keyboard()

            elif data == "topics":
                # Показать все темы
                topics = self.data_manager.get_topics()
                topics_list = "\n".join([f"• {topic.capitalize()}" for topic in topics])
                message = f"📚 Доступные темы:\n\n{topics_list}\n\nВыберите тему:"
                reply_markup = self._create_topic_keyboard()

            elif data.startswith("topic_"):
                # Факт по теме
                topic = data[6:]  # Убираем "topic_"
                fact = self.data_manager.get_fact_by_topic(topic)

                if fact:
                    self.user_prefs.update_stats(user_id)
                    message = f"📖 Факт о {topic.capitalize()}:\n\n{fact}"
                    reply_markup = self._create_fact_keyboard(topic)
                else:
                    message = f"⚠️ Не удалось найти факты по теме '{topic}'."
                    reply_markup = self._create_topic_keyboard()

            elif data.startswith("fav_"):
                # Добавить в избранное
                topic = data[4:]  # Убираем "fav_"
                self.user_prefs.set_favorite_topic(user_id, topic)

                fact = self.data_manager.get_fact_by_topic(topic)
                if fact:
                    message = f"⭐ Тема '{topic.capitalize()}' добавлена в избранное!"
                    reply_markup = self._create_fact_keyboard()

            elif data == "set_favorite":
                # Установить любимую тему
                topics = self.data_manager.get_topics()
                keyboard = []

                for i in range(0, len(topics), 2):
                    row = []
                    for j in range(2):
                        if i + j < len(topics):
                            topic = topics[i + j]
                            row.append(InlineKeyboardButton(
                                topic.capitalize(),
                                callback_data=f"setfav_{topic}"
                            ))
                    if row:
                        keyboard.append(row)

                keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="settings")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                message = "⭐ Выберите любимую тему:"

            elif data.startswith("setfav_"):
                # Установить выбранную тему как любимую
                topic = data[7:]  # Убираем "setfav_"
                self.user_prefs.set_favorite_topic(user_id, topic)
                message = f"✅ Любимая тема установлена: {topic.capitalize()}"
                reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("📖 Факт по теме", callback_data=f"topic_{topic}"),
                    InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
                ]])

            elif data == "clear_favorite":
                # Очистить избранное
                self.user_prefs.set_favorite_topic(user_id, None)
                message = "✅ Любимая тема удалена."
                reply_markup = InlineKeyboardMarkup([[
                    InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
                    InlineKeyboardButton("🔙 Главная", callback_data="main_menu")
                ]])

            elif data == "settings":
                # Настройки
                favorite_topic = self.user_prefs.get_favorite_topic(user_id)

                keyboard = [
                    [InlineKeyboardButton("📚 Выбрать любимую тему", callback_data="set_favorite")],
                    [InlineKeyboardButton("🗑️ Очистить избранное", callback_data="clear_favorite")],
                    [InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)

                if favorite_topic:
                    message = f"⚙️ Настройки:\n\n⭐ Любимая тема: {favorite_topic.capitalize()}"
                else:
                    message = "⚙️ Настройки:\n\n⭐ Любимая тема: не установлена"

            elif data == "add_fact":
                # Добавить факт
                message = (
                    "📝 Добавление факта:\n\n"
                    "Используйте команду: `/add тема \"Текст факта\"`\n\n"
                    "Пример:\n"
                    "`/add животные \"Ваш интересный факт\"`\n\n"
                    "Или вернитесь назад:"
                )
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]])

            elif data == "stats":
                # Статистика
                stats = self.user_prefs.get_user_stats(user_id)
                favorite_topic = stats.get("favorite_topic")

                message = (
                    f"📊 Ваша статистика:\n\n"
                    f"👤 Пользователь: {update.effective_user.first_name}\n"
                    f"📖 Фактов просмотрено: {stats.get('total_facts', 0)}\n"
                )

                if favorite_topic:
                    message += f"⭐ Любимая тема: {favorite_topic.capitalize()}\n"
                else:
                    message += "⭐ Любимая тема: не установлена\n"

                if stats.get("last_active"):
                    try:
                        last_active = datetime.fromisoformat(stats["last_active"]).strftime("%d.%m.%Y %H:%M")
                        message += f"🕐 Последняя активность: {last_active}\n"
                    except Exception:
                        message += f"🕐 Последняя активность: {stats.get('last_active')}\n"

                keyboard = [[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

            elif data == "main_menu":
                # Главное меню
                message = (
                    f"Главное меню, {update.effective_user.first_name}! 👋\n\n"
                    "Выберите действие:"
                )

                # Сначала редактируем текст, а затем удаляем inline-клавиатуру (если нужно)
                await query.edit_message_text(message, parse_mode='Markdown')
                try:
                    await query.edit_message_reply_markup(reply_markup=self._create_fact_keyboard())
                except Exception:
                    # если не получилось убирать reply_markup — просто игнорируем
                    pass
                return


            else:
                # Неизвестная команда
                message = "⚠️ Неизвестная команда."
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]])

            # Редактируем сообщение с новым текстом и кнопками (безопасно)
            await self._safe_edit_message(query=query, text=message, reply_markup=reply_markup, parse_mode='Markdown')

        except Exception as e:
            logger.error(f"Ошибка в обработчике кнопок: {e}")
            try:
                await query.edit_message_text(
                    "⚠️ Произошла ошибка. Попробуйте еще раз.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]])
                )
            except Exception:
                # Как запасной вариант — пришлём alert
                try:
                    await query.answer("Произошла ошибка. Попробуйте еще раз.", show_alert=True)
                except Exception:
                    logger.exception("Не удалось уведомить пользователя об ошибке.")

    async def handle_keyboard_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений для кнопок клавиатуры"""
        text = update.message.text

        if text == "🎲 Случайный факт":
            await self.random_fact_command(update, context)
        elif text == "📚 Выбрать тему":
            await self.topics_command(update, context)
        elif text == "📖 Все темы":
            await self.topics_command(update, context)
        elif text == "⭐ Мой факт":
            await self.myfact_command(update, context)
        elif text == "⚙️ Настройки":
            await self.settings_command(update, context)
        elif text == "📊 Статистика":
            await self.stats_command(update, context)
        elif text == "📝 Добавить факт":
            await self.add_fact_command(update, context)
        elif text == "❓ Помощь":
            await self.help_command(update, context)
        else:
            # Пытаемся найти факт по теме
            fact = self.data_manager.get_fact_by_topic(text.lower())
            if fact:
                user_id = update.effective_user.id
                self.user_prefs.update_stats(user_id)

                message = f"📖 Факт о {text.capitalize()}:\n\n{fact}"
                reply_markup = self._create_fact_keyboard(text.lower())

                await update.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    f"🤔 Не понял ваше сообщение.\n\n"
                    f"Попробуйте:\n"
                    f"• Нажать на кнопку ниже\n"
                    f"• Использовать команду /help\n"
                    f"• Написать название темы (например, 'животные')", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔙 Главная", callback_data="main_menu")]])
                )


    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок бота"""
        logger.error(f"Ошибка при обработке обновления: {context.error}")

        try:
            if update and getattr(update, "effective_message", None):
                await update.effective_message.reply_text(
                    "⚠️ Произошла непредвиденная ошибка.\n"
                    "Пожалуйста, попробуйте еще раз.",
                    reply_markup=self._create_main_keyboard()
                )
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения об ошибке: {e}")

    def run(self):
        """Запускает бота"""
        logger.info("Бот запущен...")
        # используем простой run_polling()
        self.application.run_polling()


def main():
    """Основная функция запуска бота"""

    # Получаем токен бота из переменных окружения (безопаснее, чем хардкод)
    TOKEN = "7533370824:AAFsrYHcHVhxwQCzl9_CzkX_3n2wFGLLLhQ"

    try:
        # Создаем и запускаем бота
        bot = FactsBot(TOKEN)
        bot.run()

    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}")
        print(f"❌ Ошибка запуска бота: {e}")


if __name__ == "__main__":
    main()

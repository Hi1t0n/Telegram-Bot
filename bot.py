from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# список вопросов и ответов
questions = [
    {
        "question": "В каком году была принята действующая Конституция РФ?",
        "options": ["В 1977 году", "В 1993 году", "В 2001 году", "В 1999 году"],
        "answer": "2"
    },
    {
        "question": "На территории Российской Федерации высшую юридическую силу имеет?",
        "options": ["Федеральный закон", "Указ Президента РФ", "Конституция РФ", "Судебная система РФ"],
        "answer": "3"
    },
    {
        "question": "Что является обязанностью государства?",
        "options": ["Защита гражданина", "Материальное обеспечение гражданина", "Признание, соблюдение и защита прав и свобод человека и гражданина"],
        "answer": "3"
    },
    {
        "question": "Кто осуществляет государственную власть в Российской Федерации?",
        "options": ["Президент РФ", "Президент РФ, Федеральное Собрание (Совет Федерации и Государственная Дума), Правительство РФ, суды РФ", "Президент РФ, Правительство РФ", "Правительство РФ"],
        "answer": "2"
    },
    {
        "question": "Государственная власть в Российской Федерации осуществляется на основе?",
        "options": ["Законодательной власти", "Разделения на законодательную и судебную власть", "Разделения на законодательную, исполнительную и судебную власть"],
        "answer": "3"
    },
    {
        "question": "Высшим непосредственным выражением власти народа являются?",
        "options": ["Референдум, свободные выборы", "Собрания, митинги", "Свободные выборы"],
        "answer": "1"
    },
    {
        "question": "Каждый имеет право на?",
        "options": ["Неприкосновенность частной жизни, личную и семейную тайну, защиту своей чести и доброго имени", "Тайну переписки, телефонных переговоров, почтовых, телеграфных и иных сообщений", "Все вышеперечисленное"],
        "answer": "3"
    },
    {
        "question": "Основные права и свободы человека и гражданина принадлежат каждому?",
        "options": ["С 14 лет", "С 18 лет", "От рождения"],
        "answer": "3"
    },
    {
        "question": "Все субъекты России во взаимоотношениях с федеральными органами государственной власти…",
        "options": ["Подчиняются федеральному центру", "Между собой равноправны", "Не зависят от федерального центра"],
        "answer": "2"
    },
    {
        "question": "Разрешает ли Конституция России смертную казнь?",
        "options": ["Нет", "Разрешает, она устанавливается федеральным законом, но в России на смертную казнь наложен мораторий", "Она разрешена и действует в настоящее время"],
        "answer": "2"
    }
]

# функция-обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот с тестом на знание Конституции РФ. Напиши /test, чтобы начать.")

# функция-обработчик команды /test
def test(update, context):
    # создаем новую сессию тестирования
    context.user_data['score'] = 0
    context.user_data['current_question'] = 0

    # отправляем первый вопрос
    send_question(update, context)

# функция-обработчик сообщений
def message(update, context):
    # получаем ответ пользователя
    answer = update.message.text

    # проверяем ответ и отправляем следующий вопрос
    if answer == questions[context.user_data['current_question']]['answer']:
        context.user_data['score'] += 1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Правильно!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неправильно.")

    context.user_data['current_question'] += 1

    if context.user_data['current_question'] < len(questions):
        send_question(update, context)
    else:
        end_test(update, context)

# функция-отправитель вопроса
def send_question(update, context):
    question = questions[context.user_data['current_question']]
    options = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(question['options'])])

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{question['question']}\n\n{options}")

# функция-завершитель теста
def end_test(update, context):
    score = context.user_data['score']
    total = len(questions)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Тест завершен! Ваш результат: {score}/{total}")
updater = Updater(token='Your token', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, end_test))
updater.start_polling()

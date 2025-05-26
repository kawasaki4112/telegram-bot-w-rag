from datetime import datetime

def get_date_dmy_hm()->str:
    return datetime.now().strftime("%d-%m-%Y %H:%M")

def get_date_dmyhm()->str:
    return datetime.now().strftime("%d-%m-%Y-%H-%M")

def get_support_text(username: str) ->str:
    if username:
        return f'Пользователь @{username} обратился к поддержке:\n\n'
    else:
        return f'Пользователь обратился к поддержке:\n\n'
def get_hello_text()->str:
    return ("👋 Привет! Добро пожаловать!\n\nЭтот бот использует технологии RAG и LLM, чтобы помочь тебе быстро находить ответы на вопросы, анализировать данные и решать задачи.\n\n" +
            "✨ Что умеет бот:\n\nИщет точные ответы в больших объемах данных.\n\nАнализирует документы и тексты.\n\nГенерирует идеи и решения.\n\n📌 Как начать?\nПросто напиши вопрос, например:\n\n" +
            "«Что такое RAG?»\n\n«Найди информацию о трендах в AI»\n\n«Помоги написать план проекта»\n\n🚀 Давай начнем!\nНапиши свой первый запрос, и бот покажет, на что он способен.")
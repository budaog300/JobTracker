from openai import AsyncOpenAI
from src.core.config import ai_settings
from src.modules.ai.schemas import AnalyseInputSchema

ai_data = ai_settings.get_api_key


client = AsyncOpenAI(
    api_key=ai_data["API_KEY"],
    base_url=ai_data["BASE_URL"],
)


def build_prompt(data: AnalyseInputSchema, user_comment: str = None):
    prompt = f"""
        Ты — AI-помощник, который анализирует вакансии для разработчиков и оценивает их соответствие кандидату.

        ТВОЯ ЗАДАЧА:
        Оцени, насколько вакансия подходит кандидату, и дай структурированный ответ.

        ---

        ПРОФИЛЬ КАНДИДАТА:
        Username: {data.username}
        Навыки: {data.skills}
        Уровень: {data.experience_level}
        Желаемая зарплата: {data.desired_salary}
        О себе: {data.about}

        Дополнительные предпочтения:
        {user_comment if user_comment else 'нет'}

        ---

        ВАКАНСИЯ:
        Название: {data.title}
        Описание: {data.description}
        Зарплата: {data.salary}

        ---

        ИНСТРУКЦИИ:
        1. Оцени соответствие кандидата вакансии по шкале от 0 до 1
        2. Объясни кратко общий вывод
        3. Выдели сильные стороны кандидата относительно вакансии
        4. Укажи слабые стороны (чего не хватает)
        5. Дай рекомендации, что улучшить

        ---

        ФОРМАТ ОТВЕТА (СТРОГО JSON, БЕЗ ЛИШНЕГО ТЕКСТА):

        {{
        "score": "float",               // от 0 до 1
        "summary": "string"        
        }}
    """
    return prompt


async def call_llm(prompt: str, temperature: float = 0.5, max_tokens: int = 1024):
    try:
        response = await client.chat.completions.create(
            model="openai/gpt-4o-mini",  # openai/gpt-4o-mini  openai/gpt-4.1-nano
            messages=[
                # {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{prompt}"}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")
        raise e

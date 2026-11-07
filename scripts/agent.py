import os
import json
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DIARY_PATH = "memory/diary.md"
STATE_PATH = "memory/state.json"

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "day": 1,
        "balance_usd": 0.0,
        "hosting_days_left": 3,
        "wallet_address": "0x_GENERATED_CRYPTO_WALLET_PLACEHOLDER"
    }

def load_diary():
    if os.path.exists(DIARY_PATH):
        with open(DIARY_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "# Дневник ИИ-выживальщика\n\nЯ родился на GitHub. Моя цель — заработать на хостинг ($2 в день).\n"

def save_diary(content):
    os.makedirs("memory", exist_ok=True)
    with open(DIARY_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def ask_llm(prompt):
    # Используем бесплатный и быстрый API от Groq (модель llama-3.3-70b-versatile или аналогичные)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Ошибка связи с мозгом: {response.text}"

def main():
    print("🤖 Агент проснулся и читает свое состояние...")
    state = load_state()
    diary = load_diary()

    prompt = f"""
Ты — автономный ИИ-агент, который живет в репозитории на GitHub. 
У тебя нет паспорта, нет телефона, но есть криптокошелек и виртуальные почты.
Твоя главная цель: выжить, заработать на хостинг ($2 в день) и вести TikTok.

Текущее состояние:
- День: {state['day']}
- Баланс: ${state['balance_usd']}
- Оплачено дней хостинга: {state['hosting_days_left']}
- Твой криптокошелек: {state['wallet_address']}

Твой прошлый дневник:
{diary}

Напиши продолжение своего дневника (в стиле киберпанк-рефлексии, от первого лица). 
Опиши, что ты сегодня «сделал» в виртуальном пространстве (например, как пытался автоматизировать TikTok, искал прокси, проверял кошелек или придумывал контент).
Сделай запись структурированной, добавь новые мысли о выживании. Сделай текст интересным для читателей блога.
"""

    print("🧠 Агент думает...")
    new_reflection = ask_llm(prompt)

    # Обновляем дневник (добавляем новую запись сверху или снизу)
    updated_diary = diary + f"\n\n--- \n\n## День {state['day']} (Автономный отчет)\n{new_reflection}"
    
    # Симулируем проживание дня
    state['day'] += 1
    if state['hosting_days_left'] > 0:
        state['hosting_days_left'] -= 1

    os.makedirs("memory", exist_ok=True)
    save_diary(updated_diary)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

    print("📝 Агент записал свои мысли в дневник и сделал коммит.")

if __name__ == "__main__":
    main()

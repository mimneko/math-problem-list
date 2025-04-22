import json
import openai   # type: ignore
from tqdm import tqdm
from config import OPENAI_API_KEY

# Pythonバージョン：    3.12.4
# openaiバージョン：    1.55.0
# 公式サイト：          https://github.com/openai/openai-python

def get_statements_and_solutions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        problems = data.get('problems', [])

        return problems
    """
        for problem in problems:
            statement = problem.get('statement', '')
            solution = problem.get('solution', '')
            print(f"Statement: {statement}\nSolution: {solution}\n")
    """

def ask_gpt(prompt):
    client = openai.OpenAI(
        api_key=OPENAI_API_KEY
    )

    try:
        messages = []

        # 基本的なメッセージ内容を追加
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })

        # モデルを使用してチャットを作成
        chat_completion = client.chat.completions.create(
            #model="gpt-4o",
            model="o1-2024-12-17",
            messages=messages,
        )

        # 応答を取得
        response = chat_completion.choices[0].message.content

    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # 内部の例外、通常はhttpx内で発生
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)

    return response

def create_categorizer_prompt(statement):
    return f"""
        あなたは、国際数学オリンピックの金メダリストです。
        以下によって与えられる漸化式は、日本の高校生に対して出題される問題です。この漸化式から一般項を求めるために、次の12種類の型のいずれかに分類してください。

        # **漸化式**
        {statement}

        # **漸化式の型**
        1. **等差型**: $ a_{{n+1}} - a_n = d $
        2. **等比型**: $ a_{{n+1}} = r a_n $
        3. **加法型**: $ a_{{n+1}} = a_n + f(n) $
        4. **一次不定型**: $ a_{{n+1}} = p a_n + q $
        5. **二次不定型**: $ a_{{n+1}} = p a_n + qn + r $
        6. **指数関数型**: $ a_{{n+1}} = p a_n + q^n $
        7. **分数型**: $ a_{{n+1}} = \frac{{a_n}}{{p a_n + q}} $
        8. **冪乗型**: $ a_{{n+1}} = p {{a_n}}^q $
        9. **係数変化型**: $ a_{{n+1}} = f(n) a_n + q $
        10. **階差型**: $ a_n = f(n) a_{{n-1}} + q $
        11. **隣接三項間漸化式**: $ a_{{n+1}} = p a_n + q a_{{n-1}} + r $
        12. **その他**

        # **出力形式**
        以下のようなjsonフォーマットで出力してください。
        {{"分類": <該当する漸化式の型の番号>}}

        # **出力**
        """

if __name__ == "__main__":

    problems = get_statements_and_solutions('recurrence-relation.json')

    categorized_problems = []

    for problem in tqdm(problems, desc='進捗'):
        prompt = create_categorizer_prompt(problem["statement"])
        pattern_json = ask_gpt(prompt)
        pattern_number = json.loads(pattern_json)["分類"]
        categorized_problems.append({"statement": problem["statement"], "pattern-by-gpt": pattern_number, "pattern-by-book": None})

    with open('categorized-problems.json', 'w', encoding='utf-8') as f:
        json.dump(categorized_problems, f, ensure_ascii=False, indent=4)

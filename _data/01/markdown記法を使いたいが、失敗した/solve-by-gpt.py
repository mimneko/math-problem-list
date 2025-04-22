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

def create_solver_prompt(statement):
    # https://metaskilling.blog/chatgpt-o1-toudai-math/ に、markdownに関する記述を加えた。
    return f"""
        あなたは、国際数学オリンピックの金メダリストです。
        以下の数学の問題の解答を作成してください。ただし、解答作成の際は、以下の点に留意してください。

        この問題は、日本の高校生に対して出題される問題です。したがって、解答には高校で習う程度の数学の知識のみを用いて解答してください。積分や関数の値は、log、In、exp、sqrt、sin、cosを用いて、解析的な形で必ず表現し、数値積分は用いないでください。
        この問題の解答には、基本的にプログラミングを使用せず、数学的な論理展開・式変形に基づく議論に基づいて、解答を作成してください。ただし、数式の計算や、図を描画する際には、必ずPythonのプログラミングを使用して、計算ミスが起こらないように注意してください。
        markdown形式で解答を記述し、インライン数式は「$」で、ブロック数式には「$$」で数式を囲んでください。
        図を描画する問題は、matplotlibを用いて、解答の図も作成してください。
        「全て求めよ。」という指示の問題に対しては、考え得る答えの組以外に、ほかの組み合わせが存在しないということも、数学的な議論に基づいて、証明してください。
        「であることを示せ。」という指示の問題は、証明問題です。したがって、いくつかの具体的な数値で成り立つことを証明するだけでなく、数学的な議論に基づいて、題意を満たす全ての場合について、命題が成立することを証明してください。
        以上の指示に基づいて、以下の問題の解答を作成してください:

        # 問題
        {statement}

        # 解答
        """

def create_verification_prompt(books_solution, gpts_solution):
    return f"""
        以下は漸化式の一般項を求める問題の、GPTによる解答と、問題集の解答である。
        a1からa5までの各項について、両方の解答が同じ値を与えるかどうかを検証し、結果を「True」または「False」のブール値のみで返してください。

        # GPTの解答
        {gpts_solution}

        # 問題集の解答
        {books_solution}

        # 結果
        """

if __name__ == "__main__":

    problems = get_statements_and_solutions('recurrence-relation.json')

    # XMLファイルを作成して出力
    with open('math_problems.xml', 'w', encoding='utf-8') as xml_file:
        xml_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        xml_file.write('<math_problems>\n')

        for problem in tqdm(problems, desc="進捗"):
            statement = problem.get('statement', '')
            books_solution = problem.get('solution', '')

            # GPT で解答を生成
            user_message = create_solver_prompt(statement)
            gpts_solution = ask_gpt(user_message)

            # GPTの解答が正しいか判定する
            verification_prompt = create_verification_prompt(books_solution, gpts_solution)
            is_correct = ask_gpt(verification_prompt)

            # XML形式で問題と解答をファイルに書き込む
            xml_file.write('<problem>\n')
            xml_file.write(f'<statement><![CDATA[{statement}]]></statement>\n')
            xml_file.write(f'<solution><![CDATA[{books_solution}]]></solution>\n')
            xml_file.write(f'<gpt><![CDATA[{gpts_solution}]]></gpt>\n')
            xml_file.write(f'<is_correct>{is_correct}</is_correct>\n')
            xml_file.write('</problem>\n')

        xml_file.write('</math_problems>\n')
        #exit(1)


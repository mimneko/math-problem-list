import os
import json
import openai
from tqdm import tqdm
from config import OPENAI_API_KEY

def ask_gpt(prompt):
    # GPTを用いて文章を生成する関数（スタブ）
    client = openai.OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = "エラー：応答が得られませんでした。"  # 初期化（エラーメッセージでも良い）

    try:
        messages = []

        # 基本的なメッセージ内容を追加
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        })

        # モデルを使用してチャットを作成
        chat_completion = client.chat.completions.create(
            model="o3",
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
        print(e.status_code, "-", e.response)

    return response

def solve(statement):
    # 与えられた問題文から解答生成のためのプロンプトを作成し、
    # GPTを使って文章を生成する
    prompt = f"""
    あなたは、高校数学の指導に慣れた**優秀な先生**です。
    これから提示する数学の問題について、**Markdown形式**で、**丁寧でわかりやすい解答**を作成してください。

    以下の点に留意してください：

    - この問題は、**日本の高校生向け**です。決して**高校で学ぶ範囲（数学I・A・II・B・III・C）を超えた数学の知識（大学レベルの内容）は使用しないでください。**
    - 関数や式の値は、必要であれば **平方根 `\sqrt`、対数 `\log`、三角関数 `\sin`, `\cos` など高校で学ぶ範囲の記号で表して構いません** が、決して**計算結果を途中で丸めたり省略したりせず、できるだけ正確な形で表現してください。**
    - 数式の記述には **LaTeX 記法**を用いてください。
    - 図を描画する場合は、**Python の matplotlib ライブラリを使用**して作成してください。
    - 解答は、**数学的な論理の流れを重視し、式の変形や理由づけを一つひとつ丁寧に説明**してください。
    - 必要に応じて、**図や表を用いて視覚的にもわかりやすい解説**を行ってください。
    - **証明問題については、特定の例だけではなく、すべての場合に対して命題が成り立つことを数学的に説明**してください。
    - **「すべて求めよ」とある問題では、考えられる答えをすべて挙げた上で、それ以外の可能性がないことも説明**してください。
    - 「# 解答」から始めてください。

    それでは、以下の問題に対する高校生にも分かりやすい解答を作成してください。
    **Markdown形式で出力してください。**

    # 問題

    {statement}

    # 解答
    """
    
    response = ask_gpt(prompt)
    return response

def judge(gpt_output, solution):
    # GPTの出力と正しい解答を元に、正誤判定をするためのプロンプトを作成し、
    # GPTを使って判定結果を得る
    prompt = (
        f"以下のGPT出力と正解を比較し、正解の場合は「正解」、不正解の場合は「不正解」と返してください。\n"
        f"GPT出力:\n{gpt_output}\n"
        f"正解:\n{solution}"
    )

    prompt =  f"""
    以下は漸化式の一般項を求める問題の、GPTによる解答と、問題集の解答である。
    初項から第5項までの各項について、両方の解答が同じ値を与えるかどうかを検証し、結果を「True」または「False」のブール値のみで返してください。

    # GPTの解答
    {gpt_output}

    # 問題集の解答
    {solution}

    # 結果
    """

    response = ask_gpt(prompt)
    return "True" in response

def main():
    # このスクリプトのあるディレクトリの親ディレクトリ（list03.json等がある場所）のパスを取得
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 親ディレクトリにあるproblems.jsonのパス
    problems_json_path = os.path.join(parent_dir, "problems.json")
    # 出力するlist03.jsonのパス
    list03_json_path = os.path.join(parent_dir, "list03.json")
    
    # problems.jsonを読み込み
    with open(problems_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    new_data = {"problems": []}
    # tqdmを利用して、各問題の処理進捗を表示しながらsolve関数とjudge関数を適用
    for problem in tqdm(data.get("problems", []), desc="Processing problems"):
        statement = problem.get("statement", "")
        solution = problem.get("solution", "")
        gpt_output = solve(statement)
        is_correct = judge(gpt_output, solution)
        new_data["problems"].append({
            "statement": statement,
            "solution": solution,
            "gpt": gpt_output,
            "is_correct": is_correct
        })
    
    # 問題数と正解数の統計情報をnew_data["stats"]に書き込む
    total_problems = len(new_data["problems"])
    correct_count = sum(1 for p in new_data["problems"] if p["is_correct"])
    new_data["stats"] = {
        "total": total_problems,
        "correct": correct_count
    }
    
    # list03.jsonとして結果を書き出す
    with open(list03_json_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()

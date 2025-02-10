import xml.etree.ElementTree as ET

def parse_math_problems_xml(file_path):
    # XMLファイルを読み込む
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 問題と解答のリストを作成
    problems_and_solutions = []

    # 各問題について情報を抽出
    for problem in root.findall('problem'):
        statement = problem.find('statement').text
        solution = problem.find('solution').text
        response = problem.find('response').text

        problems_and_solutions.append({
            'statement': statement,
            'solution': solution,
            'response': response
        })

    return problems_and_solutions

# XMLファイルから問題と解答を解析
problems = parse_math_problems_xml('math_problems.xml')

# 結果を表示
for problem in problems:
    print(f"Statement: {problem['statement']}")
    print(f"Solution: {problem['solution']}")
    print(f"GPT Response: {problem['response']}\n")

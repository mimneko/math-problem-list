import xml.etree.ElementTree as ET
import json

def convert_xml_to_json(xml_file, json_file):
    # XMLファイルを読み込む
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # JSONに変換するための辞書を作成する
    problems_list = []
    for problem in root.findall('problem'):
        problem_dict = {}
        problem_dict['statement'] = problem.find('statement').text
        problem_dict['solution'] = problem.find('solution').text
        problem_dict['gpt'] = problem.find('gpt').text
        problem_dict['is_correct'] = problem.find('is_correct').text == 'True'
        problems_list.append(problem_dict)

    # 辞書をJSONに変換してファイルに書き込む
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({'problems': problems_list}, f, ensure_ascii=False, indent=4)

# XMLファイルとJSONファイルのパスを指定
xml_file_path = 'math_problems.xml'
json_file_path = 'math_problems.json'

# 変換関数を呼び出す
convert_xml_to_json(xml_file_path, json_file_path)

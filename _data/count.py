import json
from collections import Counter

# JSONファイルを読み込む
with open('categorized-patterns-by-gpt.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# pattern-by-gpt と pattern-by-book が異なるエントリを見つける
mismatched_patterns = [entry for entry in data if entry['pattern-by-gpt'] != entry['pattern-by-book']]

# pattern-by-book の値のカウント
pattern_by_book_counts = Counter(entry['pattern-by-book'] for entry in data)

# 結果を表示する
mismatch_count = len(mismatched_patterns)
total_count = len(data)
mismatch_percentage = (mismatch_count / total_count) * 100

print(f'異なるパターンの割合: {mismatch_percentage:.2f}%')
print(f'異なるパターンの個数: {mismatch_count}')
print('異なるパターンのペア:')
for entry in mismatched_patterns:
    print(f"Statement: {entry['statement']}")
    print(f"pattern-by-gpt: {entry['pattern-by-gpt']}, pattern-by-book: {entry['pattern-by-book']}\n")

# pattern-by-book の値ごとのカウントを表示
print('pattern-by-book の値ごとのカウント:')
for i in range(1, 13):
    print(f'pattern-by-book {i}: {pattern_by_book_counts[i]}')
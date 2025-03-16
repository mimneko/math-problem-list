# math-problem-list

高校数学問題リスト

特に、次のような問題のみを選択した。

- 漸化式から、その一般項を求める問題
- 誘導なく直接求める問題
- 連立漸化式でなく、単独の漸化式の問題

## 作成の流れ

1. `recurrence-relation.json` に手作業で問題と解答を書き込む。
1. `solve-by-gpt.py` で GPT が `recurrence-relation.json` の問題を解き、 `math_problems.xml` に書き込む。
1. `xml2json.py` で `math_problems.xml` を `math_problems.json` に変換する。
1. `jekyll` で `math_problems.json` をもとに web ページを作成する。

## 2025-03-16追記
- $a_{n+1}=f(n)a_n+q$ 型は誘導が必要かも
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import string
import re
import nltk
import MeCab
nltk.download('wordnet')
import matplotlib.pyplot as plt  # max_iterの適切な値を見極めるために必要

# ファイルからデータを読み込む
with open('mix_text.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# テキスト前処理を行う
exclude = set(string.punctuation)
m = MeCab.Tagger("-Owakati")  # MeCabを使って日本語テキストを分かち書き

# 特定の文章を取り除く条件を設定
keywords_to_remove = ["まし","ます","する","プル","リクエスト","ない","こと","いる","なく","ませ","つい","よる","でき","その","および","べき","など","たら","そう","なさ","コード"]

# 特定の文章を取り除く
lines = [line for line in lines if all(keyword not in line for keyword in keywords_to_remove)]

def clean(doc):
    punc_free = ''.join(ch for ch in doc if ch not in exclude)
    no_digits = re.sub(r'\d+', '', punc_free)  # 数字を削除する
    no_alpha = re.sub(r'[a-zA-Z]+', '', no_digits)  # 英字を削除する
    normalized = m.parse(no_alpha).strip()
    return normalized
lines = [clean(line) for line in lines]

# 文書-単語行列の作成
vect = CountVectorizer(max_df=1.0, stop_words=None)
data = vect.fit_transform(lines)

# 最適なlearning_offsetの値をグラフから探る
likelihoods = []
max_iters_range = range(1, 51)

for max_iter in max_iters_range:
    lda = LatentDirichletAllocation(n_components=5, max_iter=max_iter,
                                    learning_method='online',
                                    learning_offset=10,
                                    random_state=0)
    lda.fit(data)
    likelihood = lda.score(data)
    likelihoods.append(likelihood)

# 学習曲線をプロット
plt.plot(max_iters_range, likelihoods, marker='o')
plt.xlabel('max_iter')
plt.ylabel('Log Likelihood')
plt.title('LDA Learning Curve')
plt.show()

# 最適なパラメータでLDAの適用と学習
lda = LatentDirichletAllocation(n_components=5, max_iter=40,
                                learning_method='online',
                                learning_offset=10,
                                random_state=0)

lda.fit(data)

# pyLDAvisを用いた可視化
pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(lda, data, vect, mds='tsne')
panel

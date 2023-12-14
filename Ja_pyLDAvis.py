import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import string
from nltk.stem.wordnet import WordNetLemmatizer
import re
import nltk
import MeCab  # 日本語形態素解析ライブラリ
nltk.download('wordnet')

# ファイルからデータを読み込む
with open('mixed.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# テキスト前処理を行う
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
m = MeCab.Tagger("-Owakati")  # MeCabを使って日本語テキストを分かち書き

# 特定の文章を取り除く条件を設定
keywords_to_remove = ["まし","ます","する","プル","リクエスト","ない","こと","いる","なく","ませ","つい","よる","でき","その","および","べき","など","たら","そう","なさ"]
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
vect = CountVectorizer(max_df=0.9, stop_words=None) # 
data = vect.fit_transform(lines)

# LDAの適用と学習
lda = LatentDirichletAllocation(n_components=4, max_iter=40, #
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

lda.fit(data)

# pyLDAvisを用いた可視化
pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(lda, data, vect, mds='tsne')
panel
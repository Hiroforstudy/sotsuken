# Get_Conversation.py
APIを使用し、任意のレポジトリのPull requestsのConversationで行われているやり取りを抽出するプログラム。
# Ja_pyLDAvis.py & Ja_pyLDAvis_plus.py
上記のプログラムで抽出されたやり取りをChatGPTを通して日本語で要約し、得られたデータセットをもとに"Jupyter Notebook上"でpyLDAvisを使用してトピックモデリングを行い、その結果を可視化するためのプログラム。Ja_pyLDAvis_plus.pyはJa_pyLDAvis.pyに適切なlearning_offsetの値をグラフを用いて調べるプログラムを足したもの。
# mix_text.txt
pyLDAvisを用いた実験に使うデータセット。15レポジトリ分のPull requestsのConversationの原文をChatGPTを通して日本語で要約して得られたもの。
# ori_mix_text.txt
15レポジトリ分のPull requestsのConversationの原文。

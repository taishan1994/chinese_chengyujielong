# coding=utf-8
import random
from trie import TrieTree

"""
成语接龙
"""


class CYJL:
    def __init__(self):
        self.word_dict = dict()
        self.char_count = dict()  # 统计每一个字开头的成语个数
        self.data = pd.read_csv("data/cycd.csv")
        self.trie = TrieTree()
        self.trie.build_trie_tree(self.data["成语"].values.tolist())


    def add(self, word):
        start = word[0]
        if start not in self.word_dict:
            self.word_dict[start] = [word]
            self.char_count[start] = 1
        else:
            self.word_dict[start].append(word)
            self.char_count[start] += 1

    def build(self):
        cys = self.data["成语"].values.tolist()
        for word in cys:
            self.add(word)


    def jl(self, simple=True):
        print("=" * 30)
        print("=== 欢迎进行西西嘛呦成语接龙游戏 ===")
        print("请选择难度（输入1（简单），输入2（困难））")
        level = input("难度：")
        if level == "2":
            simple = False
        print("=" * 30)
        mem_word = random.choice(list(self.word_dict.keys()))
        start_word = mem_word
        return_word = None
        start = True  # 初始化的状态
        print("出题：", mem_word)
        while True:
            word = input("你的回答：")
            if word == "":
                print("请输入一个成语！！！")
                continue
            if start:
                return_words = self.word_dict[mem_word]
                mem_word = random.choice(return_words)

            if word == "提示":
                # print(mem_word)
                print("提示：成语解释--", self.data[self.data['成语'] == mem_word]["成语解释"].values.tolist()[0])
            elif word == "再提示":
                print("提示：前三个字--", self.data[self.data['成语'] == mem_word]["成语"].values.tolist()[0][:3] + '...')
            elif word == "看看":
                print(self.trie.search(mem_word[0])[:5])
            elif "介绍" in word:
                js = word.split(" ")[-1]
                js = self.data[self.data['成语'] == js]
                cols = js.columns
                print("==============================")
                for col in cols:
                    if "unnamed" in str(col).lower():
                        continue
                    print(col + "：" + str(js[col].values.tolist()[0]))
                print("==============================")
            else:
                if start and word[0] != start_word[0]:
                    print("你输入的成语不对额，请重新输入！！！")
                    continue

                if return_word and word[0] != return_word[-1]:
                    print("您的回答不正确，请重新输入")
                    continue

                try:
                    return_words = self.word_dict[word[-1]]
                    if simple:
                        return_word = random.choice(return_words)
                    else:
                        # 选择成语数目较少的字返回
                        return_words = [(word, self.char_count[word[-1]]) for word in return_words if word[-1] in self.char_count]
                        return_words = sorted(return_words, key=lambda x:x[1])
                        return_word = return_words[0][0]

                    mem_word = random.choice(self.word_dict[return_word[-1]])
                    print("西西的回答：", return_word)
                except Exception as e:
                    print(e)
                    print("哈哈，你赢了。。")

            start = False


if __name__ == '__main__':
    import pandas as pd
    from pprint import pprint
    cyjl = CYJL()
    cyjl.build()
    # pprint(cyjl.char_count)
    # pprint(cyjl.word_dict)
    cyjl.jl(simple=False)

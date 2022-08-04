# coding:utf-8
"""
利用前缀树进行搜索提示
"""


class TrieTree(object):

    def __init__(self):
        self.dict_trie = dict()

    def add_node(self, word):
        word = word.strip()
        tree = self.dict_trie
        for i in range(1, len(word)+1):
            char = word[:i]
            if char not in tree:
                tree[char] = [word]
            else:
                tree[char].append(word)


    def build_trie_tree(self, cy_list):
        """ 创建 trie 树 """
        for word in cy_list:
            self.add_node(word)

    def search(self, word):
        """ 搜索给定 word 字符串中与词典匹配的 entity，
        返回值 None 代表字符串中没有要找的实体，
        如果返回字符串，则该字符串就是所要找的词汇的类型
        """
        tree = self.dict_trie
        res = tree.get(word, None)
        return res


if __name__ == '__main__':
    import pandas as pd
    from pprint import pprint
    trie = TrieTree()
    data = pd.read_csv("data/cycd.csv")
    cys = data["成语"].values.tolist()
    trie.build_trie_tree(cys)
    # pprint(trie.dict_trie)
    print(trie.search("略"))
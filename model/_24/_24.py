# encoding:utf-8
from itertools import permutations
import math
import re


class _24(object):

    @staticmethod
    def calcuate(query):
        query = query.strip()
        my_list = re.split('[,| ]+', query)

        # 对4个整数随机排列的列表
        result = [c for c in permutations(my_list, 4)]

        symbols = ["+", "-", "*", "/"]

        list2 = []  # 算出24的排列组合的列表

        flag = False
        print(result)

        for one, two, three, four in result:
            for s1 in symbols:
                for s2 in symbols:
                    for s3 in symbols:
                        if s1 + s2 + s3 == "+++" or s1 + s2 + s3 == "***":
                            express = ["{0}{1}{2}{3}{4}{5}{6}".format(
                                one, s1, two, s2, three, s3, four)]  # 全加或者乘时，括号已经没有意义。
                        else:
                            express = [
                                "(({0}{1}{2}){3}{4}){5}{6}".format(
                                    one, s1, two, s2, three, s3, four),
                                "({0}{1}{2}){3}({4}{5}{6})".format(
                                    one, s1, two, s2, three, s3, four),
                                "(({0}{1}({2}{3}{4})){5}{6})".format(
                                    one, s1, two, s2, three, s3, four),
                                "{0}{1}(({2}{3}{4}){5}{6})".format(
                                    one, s1, two, s2, three, s3, four),
                                "{0}{1}({2}{3}({4}{5}{6}))".format(
                                    one, s1, two, s2, three, s3, four)
                            ]
                        # print(one + two + three + four)
                            if str(one) + str(two) + str(three) + str(four) == "8383":
                                print(express)

                        for e in express:
                            try:
                                # if round(eval(e), 6) == 24:
                                if math.isclose(eval(e), 24, rel_tol=1e-10):
                                    list2.append(e)
                                    flag = True
                            except ZeroDivisionError:
                                pass

        list3 = set(list2)  # 去除重复项
        return list3

# query = input("请输入第4个数字:")

# for c in list3:
#     print("YES：", c)

# if not flag:
#     print("NO！")

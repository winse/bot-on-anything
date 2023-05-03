# encoding:utf-8
from itertools import permutations
import math
import re


class Expr(object):
    def __init__(self, left=None, right=None, op=None, result=None):
        self._result = result
        self.set_expression(left, right, op)

    def set_expression(self, left_expr, right_expr, operator):
        self._left = left_expr
        self._right = right_expr
        self._operator = operator

        try:
            if Expr.hasValue(left_expr) and Expr.hasValue(right_expr):
                expression = "{} {} {}".format(
                    left_expr._result, operator, right_expr._result)
                # print(expression)
                result = eval(expression)
                if(result >= 0):
                    self._result = result
                else:  # 不考虑负数
                    self._result = None
        except(ZeroDivisionError):
            self._result = None

    @staticmethod
    def hasValue(expr):
        return expr is not None and expr._result is not None

    def __eq__(self, other):
        isNode = isinstance(other, self.__class__)
        if not isNode:
            return False

        if (
            self._operator == other._operator
            and self._result == self._result
            and (
                set([self._left, self._right]) == set([other._left, other._right]) if (
                    self._operator == '+' or self._operator == '*'
                ) else [self._left, self._right] == [other._left, other._right]
            )
        ):
            return True
        else:
            return False

    def __hash__(self) -> int:
        hash = 1
        leftHash = self._left.__hash__()
        rightHash = self._right.__hash__()
        # 满足交换律的把Hash小的放前面
        if (self._operator == '+' or self._operator == '*') and leftHash > rightHash:
            hash = 31 * hash + rightHash
            hash = 31 * hash + leftHash
        else:
            hash = 31 * hash + leftHash
            hash = 31 * hash + rightHash
        hash = 31 * hash + self._operator.__hash__()
        return hash

    def __str__(self) -> str:
        return "({}{}{})".format(self._left, self._operator, self._right)

    def __repr__(self):
        if self._operator:
            return '<Node operator="{}">'.format(self._operator)
        else:
            return '<Node value="{}">'.format(self._result)


class N(Expr):
    def __init__(self,  result):
        super().__init__(None, None, None, result)

    def __eq__(self, other):
        isTypeN = isinstance(other, self.__class__)
        if not isTypeN:
            return False

        if (self._result == self._result):
            return True
        else:
            return False

    def __hash__(self) -> int:
        return self._result.__hash__()

    def __str__(self) -> str:
        return self._result


class _24(object):

    @staticmethod
    def calcuate(query):
        query = query.strip()
        my_list = re.split('[,| ]+', query)

        # 对4个整数随机排列的列表
        result = [c for c in permutations(my_list, 4)]
        print(result)

        symbols = ["+", "-", "*", "/"]

        list2 = []  # 算出24的排列组合的列表

        for one, two, three, four in result:
            one = N(one)
            two = N(two)
            three = N(three)
            four = N(four)
            for s1 in symbols:
                for s2 in symbols:
                    for s3 in symbols:
                        if s1 + s2 + s3 == "+++" or s1 + s2 + s3 == "***":
                            # express = ["{0}{1}{2}{3}{4}{5}{6}".format(one, s1, two, s2, three, s3, four)]  # 全加或者乘时，括号已经没有意义。
                            express = [
                                Expr(
                                    Expr(Expr(one, two, s1), three, s2), four, s3)
                            ]
                        else:
                            express = [
                                # "(({0}{1}{2}){3}{4}){5}{6}".format(one, s1, two, s2, three, s3, four),
                                Expr(Expr(Expr(one, two, s1), three, s2), four, s3),
                                # "({0}{1}{2}){3}({4}{5}{6})".format(one, s1, two, s2, three, s3, four),
                                Expr(Expr(one, two, s1), Expr(
                                    three, four, s3), s2),
                                # "(({0}{1}({2}{3}{4})){5}{6})".format(one, s1, two, s2, three, s3, four),
                                Expr(Expr(one, Expr(two, three, s2), s1), four, s3),
                                # "{0}{1}(({2}{3}{4}){5}{6})".format(one, s1, two, s2, three, s3, four),
                                Expr(one, Expr(Expr(two, three, s2), four, s3), s1),
                                # "{0}{1}({2}{3}({4}{5}{6}))".format(one, s1, two, s2, three, s3, four)
                                Expr(one, Expr(two, Expr(three, four, s3), s2), s1)
                            ]

                        for e in express:
                            # if round(eval(e), 6) == 24:
                            if Expr.hasValue(e) and math.isclose(e._result, 24, rel_tol=1e-10):
                                list2.append(e)

        print("||".join(map(str, list2)))
        list3 = set(list2)  # 去除重复项
        print("||".join(map(str, list3)))
        return list(map(str, list3))

# query = input("请输入第4个数字:")

# for c in list3:
#     print("YES：", c)

# if not flag:
#     print("NO！")


# print("\n".join(_24.calcuate(" 2 10 12 5 ")))


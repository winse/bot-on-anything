# encoding:utf-8
from itertools import permutations
import math
import re


class Expr(object):
    _left: 'Expr'
    _right: 'Expr'
    _operator: str
    _result: float

    def __init__(self, left=None, right=None, op: str = None, result: float = None):
        if result is not None:
            self._result = result
        else:
            self.set_expression(left, right, op)
            # 标准化
            self.normalize()

    def normalize(self):
        # 大的在前
        if self._operator == '+' or self._operator == '*':
            if self._left._result < self._right._result:
                self.set_expression(
                    self._right,
                    self._left,
                    self._operator
                )

        # 左边括号（表达式）优先
        if not isinstance(self._right, N):  # 右边是表达式，拆成左表达式的形式
            # ? + (? - ?)
            if self._operator == '+' or self._operator == '-':
                if self._right._operator == '+' or self._right._operator == '-':
                    self.set_expression(
                        Expr(self._left, self._right._left, self._operator),
                        self._right._right,
                        self._right._operator if self._operator == '+' else (
                            '-' if self._right._operator == '+' else '+')
                    )
                    self.normalize()  # 继续处理
            # ? * (? / ?)
            elif self._operator == '*' or self._operator == '/':
                if self._right._operator == '*' or self._right._operator == '/':
                    self.set_expression(
                        Expr(self._left, self._right._left, self._operator),
                        self._right._right,
                        self._right._operator if self._operator == '*' else (
                            '/' if self._right._operator == '*' else '*')
                    )
                    self.normalize()  # 继续处理
        # 左边是表达式，+*优先 或者 大数优先
        elif not isinstance(self._left, N):
            # (? - ?) + ?
            if self._operator == '+' or self._operator == '-':
                _mid = self._left._right
                if (self._left._operator == '-' and self._operator == '+') or (self._left._operator == self._operator and self._right._result > _mid._result):
                    self.set_expression(
                        Expr(self._left._left, self._right, self._operator),
                        _mid,
                        self._left._operator)
                    self.normalize()  # 继续处理
            # (? / ?) * ?
            elif self._operator == '*' or self._operator == '/':
                _mid = self._left._right
                if (self._left._operator == '/' and self._operator == '*') or (self._left._operator == self._operator and self._right._result > _mid._result):
                    self.set_expression(
                        Expr(self._left._left, self._right,  self._operator),
                        _mid,
                        self._left._operator
                    )
                    self.normalize()  # 继续处理

        return self

    def set_expression(self, left_expr, right_expr, operator):
        self._left = left_expr
        self._right = right_expr
        self._operator = operator
        self._result = math.nan  # 设置默认值

        try:
            if Expr.hasValue(left_expr) and Expr.hasValue(right_expr):
                expression = "{} {} {}".format(
                    left_expr._result, operator, right_expr._result)
                # print(expression)

                result = eval(expression)
                if(result >= 0):  # 只考虑自然数
                    self._result = result
        except(ZeroDivisionError):
            self._result = math.nan

    @staticmethod
    def hasValue(expr):
        return expr is not None and not math.isnan(expr._result)

    def __eq__(self, other):
        isNode = isinstance(other, self.__class__)
        if not isNode:
            return False

        return (
            self._operator == other._operator
            and self._result == self._result
            and (
                set([self._left, self._right]) == set([other._left, other._right]) if (
                    self._operator == '+' or self._operator == '*'
                ) else [self._left, self._right] == [other._left, other._right]
            )
        )

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

    def __str__(self, outerOperator=None, isOuterLeftChild=None):
        return self.__repr__(outerOperator, isOuterLeftChild)

    '''
    parentOperator: 外层表达式的符号
    parentLeftChild: 在外层表达式的左边还是右边，左边是True， 右边为False
    '''

    def __repr__(self, outerOperator=None, isOuterLeftChild=None):
        # template = "{}{}{}" if self._operator == '*' or self._operator == '/' else "({}{}{})"

        template = "({}{}{})"
        # if isOuterLeftChild:
        #     if (outerOperator == '*' or outerOperator == '/') and (self._operator == '+' or self._operator == '-'):
        #         template = "({}{}{})"
        #     else:
        #         template = "{}{}{}"
        # else:
        #     if outerOperator == '/' or (outerOperator == '*' and (self._operator == '+' or self._operator == '-')) or (outerOperator == '-' and (self._operator == '+' or self._operator == '-')):
        #         template = "({}{}{})"
        #     else:
        #         template = "{}{}{}"

        return template.format(self._left.__repr__(self._operator, True), self._operator, self._right.__repr__(self._operator, False))


class N(Expr):
    def __init__(self,  result: str):
        super().__init__(None, None, None, int(result))

    def normalize(self):
        return self

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

    def __str__(self, a1=None, a2=None):
        return self.__repr__()

    def __repr__(self, a1=None, a2=None):
        return '{}'.format(str(self._result))


class _24(object):

    @staticmethod
    def calcuate(query):
        query = query.strip()
        my_list = re.split('[,| ]+', query)
        if len(my_list) != 4:
            raise ValueError("please input four number.")  

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

        print(" || ".join(map(str, list2)))
        print("---")
        list3 = set(list2)  # 去除重复项

        print(" || ".join(map(str, list3)))
        print("---")
        return list(map(str, list3))

# query = input("请输入第4个数字:")

# for c in list3:
#     print("YES：", c)

# if not flag:
#     print("NO！")


#print("\n".join(_24.calcuate(" 2 10 12 5 ")))
#print("\n".join(_24.calcuate(" 12 12 12 12  ")))
#print("\n".join(_24.calcuate(" 3 12 13 1 ")))
#print("\n".join(_24.calcuate(" 2 5 9 11 ")))
#print("\n".join(_24.calcuate(" 5, 8, 3, 4 ")))
#print("\n".join(_24.calcuate(" 13 3 4 6 ")))


# -*- coding: utf-8 -*-
# 导入 Convex_hull_UG 类
from .Convex_hull_UG import Convex_hull_UG
from .LPD_UG import LPD_UG
from .Convex_hull_DAG import Convex_hull_DAG

# 暴露 CMSA 和 IPA 函数
def CMSA(graph, r):
    # 创建 Convex_hull_UG 类的实例并调用 CMSA 方法
    convex_hull = Convex_hull_UG(graph)  # 传入图对象
    return convex_hull.CMSA(r)

def IPA(graph, r):
    # 创建 Convex_hull_UG 类的实例并调用 IPA 方法
    convex_hull = Convex_hull_UG(graph)  # 传入图对象
    return convex_hull.IPA(r)


# 可选：如果你希望直接暴露特定的函数，可以将它们作为顶层函数暴露
def CMDSA(graph, r):
    convex_hull = Convex_hull_DAG(graph)
    return convex_hull.CMDSA(r)

def Local_decom_CMSA(input_tuple):
    lpd_ug = LPD_UG(input_tuple)
    return lpd_ug.Local_decom_CMSA()

def Local_decom_IPA(input_tuple):
    lpd_ug = LPD_UG(input_tuple)
    return lpd_ug.Local_decom_IPA()# my_package/convex_hull_ug/__init__.py

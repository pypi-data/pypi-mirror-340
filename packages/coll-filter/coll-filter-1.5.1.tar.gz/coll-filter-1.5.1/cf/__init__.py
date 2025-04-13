#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import math
from enum import Enum
from typing import Iterable, Tuple, List, Mapping, Collection, Generic, TypeVar

from .utils import fusion

__all__ = ['CollFilter']


U = TypeVar('U')
T = TypeVar('T')


class CFType(Enum):
    UCF = 'UserCF'
    ICF = 'ItemCF'


def default_similar_func(items: List, other: List) -> float:
    """两个item并集数

    以用户相似度为例，遍历item_users，每行用户间拥有共同的item，避免遍历userTtems大量用户间没有共同的item：
    item1: user1, user2, user3

    user1和user2共同有item1:
    user1: item1, item2, item3
    user2: item1, item4, item5

    传入此方法的参数为:
    items: [item1, item2, item3]
    other: [item1, item4, item5]
    """
    return 1.0 / float(len(set(items + other)))


def sqrt_similar_func(items: List, other: List) -> float:
    """两个item数相乘开根"""
    return 1.0 / math.sqrt(len(items) * len(other))


class CollFilter(Generic[U, T]):
    """
    Collaborative filter

    Examples
    --------
    >>> from cf import CollFilter
    >>> data = read_data('file_path')
    >>> data = pre_process(data)  # return List[(user_id: Any, item_id: Any, rating: float)]
    >>> cf = CollFilter(data)
    >>> ucf = cf.user_cf()  # return {user_id: [(item_id, score),],}
    >>> icf = cf.item_cf()  # return {user_id: [(item_id, score),],}
    >>> recommend = cf.recommend(user_id, num_recalls=5) # return [(item_id, score),]
    >>> recommends = cf.recommends(user_ids, num_recalls=5) # return {user_id: [(item_id, score),],}
    >>> cf.release()
    """

    def __init__(self, data: Iterable[Tuple[U, T, float]], n_jobs=os.cpu_count(), row_unique=False, num_user_items=256, 
                 num_item_users=256, similar_fn=default_similar_func, cache_similar: bool = False, verbose: bool = False):
        """
        初始化协作过滤推荐系统。

        :param data: 可迭代的用户-项目-评分数据，格式为(user, item, rating)的元组。
        :param n_jobs: 并行处理的作业数量，默认为CPU核心数。
        :param row_unique: 是否确保数据中的每一行都是唯一的。
        :param num_user_items: 输入是每个用户对应的物品数。
        :param num_item_users: 输入是每个物品对应的用户数。
        :param similar_fn: 计算项目相似度的函数，默认使用`default_similar_func`。
        :param cache_similar: 是否缓存项目相似度计算结果。
        :param verbose: 是否启用详细输出模式。
        """
        # 根据n_jobs的值选择合适的协作过滤实现
        if n_jobs > 1:
            # 如果n_jobs大于1，使用多进程协作过滤实现
            from cf.pooling import PoolCollFilter
            self._coll_filter = PoolCollFilter(data, n_jobs, row_unique, num_user_items, num_item_users, similar_fn, cache_similar, verbose)
        else:
            # 如果n_jobs小于等于1，使用单进程协作过滤实现
            from cf.base import BaseCollFilter
            self._coll_filter = BaseCollFilter(data, row_unique, num_user_items, num_item_users, similar_fn, cache_similar, verbose)

    def user_cf(self,
                num_recalls=64,
                num_similar=256,
                user_ids: Collection[U] = None,
                user_similar: Mapping[U, Mapping[U, float]] = None,
                similar_fn=None,
                similar_batch_size: int = 512,
                cf_batch_size: int = 128
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        基于用户的协同过滤
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个用户最大相似用户个数
        @param user_ids  要推荐的用户列表
        @param user_similar  用户相似矩阵
        @param similar_fn  相似度计算函数
        @param similar_batch_size  相似度计算函数每次计算的数据量
        @param cf_batch_size  协同过滤计算每次计算的数据量
        @return {user_id: [(item_id, score),],}
        """
        assert num_recalls > 0, "'num_recalls' should be a positive number."
        return self._coll_filter.user_cf(num_recalls, num_similar, user_ids, user_similar, similar_fn, similar_batch_size, cf_batch_size)

    def item_cf(self,
                num_recalls=64,
                num_similar=256,
                user_ids: Collection[U] = None,
                item_similar: Mapping[T, Mapping[T, float]] = None,
                similar_fn=None,
                similar_batch_size: int = 256,
                cf_batch_size: int = 128
                ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        基于物品的协同过滤
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param user_ids  要推荐的用户列表
        @param item_similar  物品相似矩阵
        @param similar_fn  相似度计算函数
        @param similar_batch_size  相似度计算函数每次计算的数据量
        @param cf_batch_size  协同过滤计算每次计算的数据量
        @return {user_id: [(item_id, score),],}
        """
        assert num_recalls > 0, "'num_recalls' should be a positive number."
        return self._coll_filter.item_cf(num_recalls, num_similar, user_ids, item_similar, similar_fn, similar_batch_size, cf_batch_size)

    def recommend(self, user_id: U, num_recalls=64, num_similar=8, similar_fn=None, ratio=0.5, return_score=False,
                batch_size: int = 256) -> List[Tuple[T, float]]:
        """
        给一个用户推荐
        @param user_id  要推荐的用户
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @param return_score 是否返回分数
        @return [item_id,] or [(item_id, score),]
        """
        result = self._recommend(user_id, num_recalls, num_similar, similar_fn, ratio, batch_size)
        return result if return_score else [item[0] for item in result]

    def _recommend(self, user_id: U, num_recalls, num_similar, similar_fn, ratio,
                batch_size: int) -> List[Tuple[T, float]]:
        """
        给一个用户推荐
        @param user_id  要推荐的用户
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @return [(item_id, score),]
        """
        icf = self.item_cf(num_recalls, num_similar, [user_id], None, similar_fn, batch_size)
        icf_items = icf[user_id]
        if num_recalls == 1:
            if icf_items:
                return icf_items
            else:
                return self.user_cf(num_recalls, num_similar, [user_id], None, similar_fn, batch_size)[user_id]
        else:
            ucf_items = self.user_cf(num_recalls, num_similar, [user_id], None, similar_fn, batch_size)[user_id]
            return fusion(icf_items, ucf_items, num_recalls, ratio)

    def recommends(self,
                   user_ids: Collection[U] = None,
                   num_recalls: int = 64,
                   num_similar: int = 8,
                   similar_fn=None,
                   ratio: float = 0.5,
                batch_size: int = 256
                   ) -> Mapping[U, List[Tuple[T, float]]]:
        """
        给一批用户推荐
        @param user_ids  要推荐的用户列表，如果为空给所有用户推荐
        @param num_recalls  每个用户最大召回个数
        @param num_similar  每个物品最大相似物品个数
        @param similar_fn  相似度计算函数
        @param ratio  推荐结果中item_cf所占比例
        @return {user_id: [(item_id, score),],}
        """
        icf = self.item_cf(num_recalls, num_similar, user_ids, None, similar_fn, batch_size)
        if num_recalls == 1:
            user_similar = self.get_user_similar(num_similar, similar_fn, batch_size)
            for user_id, items in icf.items():
                if not items:
                    icf[user_id] = self.user_cf(num_recalls, num_similar, [user_id], user_similar, similar_fn, batch_size)[user_id]
        else:
            ucf = self.user_cf(num_recalls, num_similar, user_ids, None, similar_fn, batch_size)
            for user_id, icf_items in icf.items():
                ucf_items = ucf[user_id]
                icf[user_id] = fusion(icf_items, ucf_items, num_recalls, ratio)

        return icf

    def get_user_similar(self, num_similar=256, similar_fn=None,
                batch_size: int = 512) -> Mapping[U, Mapping[U, float]]:
        """
        用户相似矩阵
        """
        return self._coll_filter.cal_similar(CFType.UCF, num_similar, similar_fn, batch_size)

    def get_item_similar(self, num_similar=256, similar_fn=None,
                batch_size: int = 512) -> Mapping[T, Mapping[T, float]]:
        """
        物品相似矩阵
        """
        return self._coll_filter.cal_similar(CFType.ICF, num_similar, similar_fn, batch_size)

    def release(self):
        self._coll_filter.release()

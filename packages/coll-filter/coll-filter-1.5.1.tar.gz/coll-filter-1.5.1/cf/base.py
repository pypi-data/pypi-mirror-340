#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""base_coll_filter, one process"""

import os
import time
import math
from collections import defaultdict
from typing import Iterable, Mapping, Tuple, Generic

from . import default_similar_func, CFType, U, T
from .utils import print_cost_time, sort_similar, logger


class CollFilterHelper:
    """
    使用用户协同过滤的方法为用户生成商品推荐列表。

    参数:
    user_item_ratings: 字典，{用户ID: {商品ID: 评分}}，表示用户对商品的评分。
    similar_dict: 字典，{用户ID: [(用户ID, 相似度)]}，表示用户之间的相似度。
    user_items_list: 列表，[(用户ID, [商品ID])]，表示用户已经消费的商品列表。
    num_recalls: 整数，推荐的商品数量。

    返回:
    字典，{用户ID: [(商品ID, 推荐分数)]}，表示为每个用户推荐的商品列表。
    """
    @staticmethod
    def _do_user_cf(user_item_ratings, similar_dict, user_items_list, num_recalls, verbose: bool):
        if verbose:
            logger.info(f"\t进程 <{os.getpid()}> 开始 处理 {len(user_items_list)} 条记录...")
        start_time = time.perf_counter()
        result = {}
        for user_id, items in user_items_list:
            item_score = {}  # {item: score}
            # {user_id: [(user_id: similar),],}  用户间的相似度
            user_similar = similar_dict.get(user_id, [])
            for u2, similar in user_similar:  # 遍历相似度用户列表
                user_item_rating = user_item_ratings.get(u2, {})
                for item, rating in user_item_rating.items():  # 逐个获取相似用户的item列表
                    if item in items:  # item不在用户已消费的列表里
                        continue
                    item_score[item] = item_score.get(item, 0.0) + math.sqrt(similar * rating)
            if len(item_score) > 0:
                result[user_id] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:num_recalls]
            else:
                result[user_id] = []

        print_cost_time(f"\t进程 <{os.getpid()}> 完成 处理 {len(user_items_list)} 条记录, 生成 {len(result)} 条记录, 耗时", start_time)
        return result

    @staticmethod
    def _do_item_cf(_user_item_ratings, similar_dict, user_items_list, num_recalls, verbose: bool):
        if verbose:
            logger.info(f"\t进程 <{os.getpid()}> 开始 处理 {len(user_items_list)} 条记录...")
        start_time = time.perf_counter()
        result = {}
        for user_id, item_ratings in user_items_list:
            item_score = {}  # {item: score}
            for item, rating in item_ratings.items():  # 遍历用户已消费的item
                # {item_id: similar,}
                item_similar = similar_dict.get(item, [])
                for item2, similar in item_similar:  # 与用户已消费item相似的item
                    if item2 in item_ratings:
                        continue
                    item_score[item2] = item_score.get(item2, 0.0) + math.sqrt(similar * rating)
            if len(item_score) > 0:
                result[user_id] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:num_recalls]
            else:
                result[user_id] = []

        print_cost_time(f"\t进程 <{os.getpid()}> 完成 处理 {len(user_items_list)} 条记录, 生成 {len(result)} 条记录, 耗时", start_time)
        return result


class BaseCollFilter(CollFilterHelper, Generic[U, T]):

    def __init__(self, data: Iterable[Tuple[U, T, float]], row_unique=False, num_user_items=128, num_item_users=128,
                 similar_fn=default_similar_func, cache_similar: bool = False, verbose: bool = False):
        self.similar_fn = similar_fn
        self.verbose = verbose
        # {user_id: {item_id: rating},}  {item_id: {user_id: rating},}
        self.user_item_ratings, item_user_ratings = defaultdict(dict), defaultdict(dict)
        start_time = time.perf_counter()
        cnt = 0
        if row_unique:
            for user_id, item_id, rating in data:
                cnt += 1
                self.user_item_ratings[user_id][item_id] = rating
                item_user_ratings[item_id][user_id] = rating
        else:
            for user_id, item_id, rating in data:
                cnt += 1
                self.user_item_ratings[user_id][item_id] = self.user_item_ratings[user_id].get(item_id, 0) + rating
                item_user_ratings[item_id][user_id] = item_user_ratings[item_id].get(user_id, 0) + rating
        if num_user_items > 0:
            self.user_items = dict([(user_id, [item[0] for item in list(sorted(items.items(), key=lambda x: x[1], reverse=True))[:num_user_items]]) for user_id, items in self.user_item_ratings.items()])
        else:
            self.user_items = dict([(user_id, [item[0] for item in items.items()]) for user_id, items in self.user_item_ratings.items()])
        if num_item_users > 0:
            self.item_users = dict([(item_id, [user[0] for user in list(sorted(users.items(), key=lambda x: x[1], reverse=True))[:num_item_users]]) for item_id, users in item_user_ratings.items()])
        else:
            self.item_users = dict([(item_id, [user[0] for user in users.items()]) for item_id, users in item_user_ratings.items()])
            
        self._cache_similar = cache_similar
        if cache_similar:
            self._user_similar_cache, self._item_similar_cache = None, None

        print_cost_time(f"数据处理, 当前进程 <{os.getpid()}> 完成 处理 {cnt} 条记录, "
                        f"user数: {len(self.user_item_ratings)}, item数: {len(self.item_users)}, 耗时", start_time)
        logger.info("=" * 90)
        
    def user_cf(self, num_recalls=10, num_similar=256, user_ids=None, user_similar=None, similar_fn=None, 
                similar_batch_size: int = 2024, cf_batch_size: int = 128):
        """
        用户协同过滤

        @param num_recalls  每个用户推荐结果数目
        @param num_similar  用户相似矩阵最大个数
        @param user_ids  要推荐的用户列表
        @param user_similar  用户相似矩阵
        @param similar_fn  相似度计算函数
        @param similar_batch_size  相似度计算函数每次计算的数据量
        @param cf_batch_size  协同过滤计算每次计算的数据量
        @return {user_id: [(item, score),],}
        """
        user_similar = user_similar or self.cal_similar(CFType.UCF, num_similar, similar_fn, similar_batch_size)
        return self._cf(user_ids, user_similar, num_recalls, CFType.UCF, cf_batch_size)

    def item_cf(self, num_recalls=10, num_similar=256, user_ids=None, item_similar=None, similar_fn=None,
                 similar_batch_size: int = 2024, cf_batch_size: int = 128):
        """
        物品协同过滤

        @param num_recalls  每个用户推荐结果数目
        @param num_similar  物品相似矩阵最大个数
        @param user_ids  要推荐的用户列表
        @param item_similar  物品相似矩阵
        @param similar_fn  相似度计算函数
        @param similar_batch_size  相似度计算函数每次计算的数据量
        @param cf_batch_size  协同过滤计算每次计算的数据量
        @return {user_id: [(item, score),],}
        """
        item_similar = item_similar or self.cal_similar(CFType.ICF, num_similar, similar_fn, similar_batch_size)
        return self._cf(user_ids, item_similar, num_recalls, CFType.ICF, cf_batch_size)

    def cal_similar(self, cf_type: CFType, num_similar=256, similar_fn=None, batch_size: int = 2024):
        """
        计算相似度

        @return dict{:List()}    {user1: {user2: similar}}
        """
        if self._cache_similar:
            if CFType.UCF == cf_type:
                if not self._user_similar_cache:
                    self._user_similar_cache = self._cal_similar(cf_type, num_similar, similar_fn, batch_size)
                return self._user_similar_cache
            else:
                if not self._item_similar_cache:
                    self._item_similar_cache = self._cal_similar(cf_type, num_similar, similar_fn, batch_size)
                return self._item_similar_cache
        else:
            return self._cal_similar(cf_type, num_similar, similar_fn, batch_size)

    def release(self):
        del self.user_item_ratings, self.user_items, self.item_users
        if self._cache_similar:
            del self._user_similar_cache, self._item_similar_cache

    def _cal_similar(self, cf_type: CFType, num_similar, similar_fn, batch_size: int):
        """
        计算相似度

        @return dict{:List()}    {user1: {user2: similar}}
        """
        logger.info(f'开始{cf_type.value[:-2]}相似度计算, num_similar = {num_similar}')
        func_start_time = time.perf_counter()
        dict1, items_list = self._get_cal_similar_inputs(cf_type)
        similar_fn = similar_fn or self.similar_fn
        similar = self._do_cal_similar(dict1, items_list, similar_fn, self.verbose)
        similar = sort_similar(similar, num_similar)
        print_cost_time(f"完成{cf_type.value[:-2]}相似度计算, 当前进程 <{os.getpid()}> 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        logger.info("=" * 90)
        return similar

    def _get_cal_similar_inputs(self, cf_type: CFType):
        if cf_type == CFType.UCF:
            return self.user_items, self.item_users.values()
        else:
            return self.item_users, self.user_items.values()

    @staticmethod
    def _do_cal_similar(dict1: Mapping, items_list: list[Iterable], similar_func, verbose: bool):
        if verbose:
            logger.info(f"\t进程 <{os.getpid()}> 开始 处理 {len(items_list)} 条记录...")
        start_time = time.perf_counter()
        similar = defaultdict(dict)

        for items in items_list:
            if len(items) <= 1:
                continue

            for item1 in items:
                for item2 in items:
                    if item1 == item2:
                        continue
                    # 计算两个item间的相似性
                    similar[item1][item2] = similar[item1].get(item2, 0.0) + similar_func(dict1.get(item1, []), dict1.get(item2, []))
        print_cost_time(f"\t进程 <{os.getpid()}> 完成 生成 {len(similar)} 条记录, 耗时", start_time)
        return similar

    def _cf(self, user_ids, similar_dict, num_recalls, cf_type: CFType, batch_size: int):
        logger.info(f'开始{cf_type.value}推理, num_recalls = {num_recalls}')
        func_start_time = time.perf_counter()
        if user_ids:
            if not set(user_ids).intersection(self.user_item_ratings.keys()):
                return {user_id: [] for user_id in user_ids}

            user_items_list = [(user_id, self.user_item_ratings.get(user_id, {})) for user_id in user_ids]
        else:
            user_items_list = self.user_item_ratings.items()

        if cf_type == CFType.UCF:
            cf_result = self._do_user_cf(self.user_item_ratings, similar_dict, user_items_list, num_recalls, self.verbose)
        else:
            cf_result = self._do_item_cf(self.user_item_ratings, similar_dict, user_items_list, num_recalls, self.verbose)
        print_cost_time(f"完成{cf_type.value}推理, 当前进程 <{os.getpid()}> 完成 生成{len(cf_result)}条记录, 总耗时", func_start_time)
        logger.info("=" * 90)
        return cf_result


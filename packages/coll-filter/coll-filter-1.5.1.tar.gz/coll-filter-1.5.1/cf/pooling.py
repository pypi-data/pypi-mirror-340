#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""pool_coll_filter"""

import os
import time
import math
# from multiprocessing import Pool
from typing import Iterable, Tuple
from concurrent.futures import as_completed, ProcessPoolExecutor
from .base import BaseCollFilter
from . import default_similar_func, CFType, U, T
from .utils import print_cost_time, sort_similar, logger


class PoolMultiProcessor:

    def __init__(self, n_jobs):
        self.n_jobs = n_jobs if n_jobs > 1 else os.cpu_count()

    def _cal_similar_batch_params(self, size: int, batch_size: int) -> Tuple[int, int]:
        """
        计算并行处理的批次参数。

        Args:
            size: 总任务数。
            batch_size: 初始批次大小。

        Returns:
            一个元组，包含调整后的批次大小和作业数。
        """
        # 计算需要的作业数 n_jobs，基于任务总数 size 和每批次的任务数 batch_size。
        n_jobs = math.ceil(size / batch_size)
        # 将 n_jobs 限制在用户指定的最大作业数 self.n_jobs 内。
        n_jobs = min(n_jobs, self.n_jobs)
        # 计算每个作业的分割大小 split_size，确保每个作业可以进一步细分为更小的批次。
        if n_jobs > 1:
            split_size = math.ceil(size / (n_jobs << 1))
            batch_size = min(max(batch_size, split_size), batch_size << 4)
        else:
            batch_size = size
       
        logger.info(f"总记录数: {size}, n_jobs: {n_jobs}, batch_size: {batch_size}")
        return batch_size, n_jobs
    
    def _cal_cf_batch_params(self, size: int, batch_size: int) -> Tuple[int, int]:
        """
        计算并行处理的批次参数。

        Args:
            size: 总任务数。
            batch_size: 初始批次大小。

        Returns:
            一个元组，包含调整后的批次大小和作业数。
        """
        # 计算需要的作业数 n_jobs，基于任务总数 size 和每批次的任务数 batch_size。
        n_jobs = math.ceil(size / batch_size)
        # 将 n_jobs 限制在用户指定的最大作业数 self.n_jobs 内。
        n_jobs = min(n_jobs, self.n_jobs)
        # 计算每个作业的分割大小 split_size，确保每个作业可以进一步细分为更小的批次。
        if n_jobs > 1:
            split_size = math.ceil(size / (n_jobs << 1))
            batch_size = min(max(batch_size, split_size), batch_size << 1)
        else:
            batch_size = size
       
        logger.info(f"总记录数: {size}, n_jobs: {n_jobs}, batch_size: {batch_size}")
        return batch_size, n_jobs
    
    def cal_similar(self, dict1, items_list, cal_fn, similar_fn, batch_size: int, verbose: bool):
        size = len(items_list)
        batch_size, n_jobs = self._cal_similar_batch_params(size, batch_size)

        # results = [self.pool.apply_async(func=cal_fn, args=(dict1, items_list[i:i+split_size], similar_fn))
        #            for i in range(split_size, size, split_size)]
        
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = [executor.submit(cal_fn, dict1, items_list[i:i+batch_size], similar_fn, verbose)
                    for i in range(0, size, batch_size)]

        similar = {}
        for result in as_completed(results):
            # for key, items in result.get().items():
            for key, items in result.result().items():
                if key in similar:
                    for item, score in items.items():
                        similar[key][item] = similar[key].get(item, 0.0) + score
                else:
                    similar[key] = items

        return similar

    def cf(self, user_item_ratings, user_items_list, similar_dict, num_recalls, cf_fn, batch_size: int, verbose: bool):
        size = len(user_items_list)
        batch_size, n_jobs = self._cal_cf_batch_params(size, batch_size)

        # results = [self.pool.apply_async(func=cf_fn,
        #                                  args=(user_item_ratings,
        #                                        similar_dict,
        #                                        user_items_list[i:i + split_size],
        #                                        num_recalls
        #                                        )
        #                                  )
        #            for i in range(split_size, size, split_size)]
        
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            results = [executor.submit(cf_fn, user_item_ratings, similar_dict, user_items_list[i:i + batch_size], num_recalls, verbose)
                    for i in range(0, size, batch_size)]

        # cf_result = cf_fn(user_item_ratings, similar_dict, user_items_list[:split_size], num_recalls, verbose)

        cf_result = {}
        for result in as_completed(results):
            # cf_result.update(result.get())
            cf_result.update(result.result())

        return cf_result


class PoolCollFilter(BaseCollFilter):

    def __init__(self, data: Iterable[Tuple[U, T, float]], n_jobs=0, row_unique=False, num_user_items=128, num_item_users=128,
                 similar_fn=default_similar_func, cache_similar: bool = False, verbose: bool = False):
        super().__init__(data, row_unique, num_user_items, num_item_users, similar_fn, cache_similar, verbose)
        self.processor = PoolMultiProcessor(n_jobs)

    def release(self):
        super().release()

    def _cal_similar(self, cf_type: CFType, num_similar, similar_fn, batch_size: int):
        """
        计算相似度

        @return dict{:dict}    {user1: {user2: similar}}
        """
        logger.info(f'开始{cf_type.value[:-2]}相似度计算, num_similar: {num_similar}')
        func_start_time = time.perf_counter()
        dict1, items_list = self._get_cal_similar_inputs(cf_type)
        items_list = list(items_list)
        items_len = len(items_list)
        similar_fn = similar_fn or self.similar_fn
        if items_len < 256:
            similar = self._do_cal_similar(dict1, items_list, similar_fn, self.verbose)
        else:
            similar = self.processor.cal_similar(dict1, items_list, self._do_cal_similar, similar_fn, batch_size, self.verbose)
        similar = sort_similar(similar, num_similar)
        print_cost_time(f"完成{cf_type.value[:-2]}相似度计算, 当前进程 <{os.getpid()}>, 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        logger.info("=" * 90)
        return similar

    def _cf(self, user_ids, similar_dict, num_recalls, cf_type: CFType, batch_size: int):
        logger.info(f'开始{cf_type.value}推理, num_recalls: {num_recalls}')
        if not similar_dict:
            logger.info(f'{cf_type.value}相似度为空, 无法进行推荐')
            return {}
        func_start_time = time.perf_counter()
        if user_ids:
            if not set(user_ids).intersection(self.user_item_ratings.keys()):
                return {user_id: [] for user_id in user_ids}

            user_items_list = list(map(lambda x: (x, self.user_item_ratings.get(x, [])), user_ids))
        else:
            user_items_list = list(self.user_item_ratings.items())

        user_items_len = len(user_items_list)
        cf_func = self._do_user_cf if cf_type == CFType.UCF else self._do_item_cf
        if user_items_len >= batch_size:
            cf_result = self.processor.cf(self.user_item_ratings, user_items_list, similar_dict, num_recalls, cf_func, batch_size, self.verbose)
        else:
            cf_result = cf_func(self.user_item_ratings, similar_dict, user_items_list, num_recalls, self.verbose)
        print_cost_time(f"完成{cf_type.value}推理, 当前进程 <{os.getpid()}>, 生成{len(cf_result)}条记录, 总耗时", func_start_time)
        logger.info("=" * 90)
        return cf_result


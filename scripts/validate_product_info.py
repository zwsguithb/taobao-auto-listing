#!/usr/bin/env python3
"""
淘宝商品上架资料校验工具
读取商品资料CSV，校验必填项完整性，输出上架准备报告。

用法:
    python3 validate_product_info.py <csv_file_path>
"""

import csv
import sys
import os

REQUIRED_FIELDS = [
    "商品标题",
    "商品类目",
    "主图路径1",
    "一口价",
    "总库存",
    "运费模板",
    "发货时间",
]

OPTIONAL_BUT_RECOMMENDED = [
    "品牌",
    "核心属性",
    "详情图路径",
    "商家编码",
]


def validate_file(filepath):
    if not os.path.exists(filepath):
        print(f"[错误] 文件不存在: {filepath}")
        return False

    if not filepath.lower().endswith(".csv"):
        print(f"[警告] 文件不是CSV格式: {filepath}")

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("[错误] CSV文件为空，没有商品数据")
        return False

    print(f"共读取 {len(rows)} 个商品资料\n")
    print("=" * 60)

    all_pass = True
    for idx, row in enumerate(rows, 1):
        title = row.get("商品标题", "(无标题)")
        print(f"\n【商品 {idx}】{title[:40]}")
        print("-" * 40)

        missing = []
        for field in REQUIRED_FIELDS:
            val = row.get(field, "").strip()
            if not val:
                missing.append(field)

        if missing:
            print(f"  [缺失必填项] {', '.join(missing)}")
            all_pass = False
        else:
            print("  [必填项] 全部齐全 ✓")

        # 检查主图文件是否存在
        for i in range(1, 6):
            key = f"主图路径{i}"
            path = row.get(key, "").strip()
            if path and not os.path.exists(path):
                print(f"  [图片不存在] {key}: {path}")
                all_pass = False

        # 检查详情图路径
        detail = row.get("详情图路径", "").strip()
        if detail and not os.path.exists(detail):
            print(f"  [详情图路径不存在] {detail}")

        # 推荐项提示
        weak = []
        for field in OPTIONAL_BUT_RECOMMENDED:
            if not row.get(field, "").strip():
                weak.append(field)
        if weak:
            print(f"  [建议补充] {', '.join(weak)}")

        # SKU检查
        sku_name = row.get("SKU规格名称", "").strip()
        sku_value = row.get("SKU规格值", "").strip()
        if sku_name and not sku_value:
            print(f"  [警告] 设置了规格名称「{sku_name}」但未填写规格值")

    print("\n" + "=" * 60)
    if all_pass:
        print("校验完成：所有商品必填项齐全，可以开始上架。")
    else:
        print("校验完成：存在缺失项，请补充后再上架。")
    return all_pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 validate_product_info.py <csv_file_path>")
        sys.exit(1)
    success = validate_file(sys.argv[1])
    sys.exit(0 if success else 1)

import logging
import argparse
import sys
import os
import pdb  # 添加pdb导入
import json
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """airplane_mbse包的主入口点。"""
    parser = argparse.ArgumentParser(description="SysML自扩展知识库")
    parser.add_argument("--init-db", action="store_true", help="初始化数据库")
    parser.add_argument("--model", type=str, help="按名称建模系统")
    parser.add_argument(
        "--auto-expand",
        action="store_true",
        help="建模时自动扩展子系统",
    )
    parser.add_argument(
        "--global-modeling",
        action="store_true",
        help="启动全局自动建模功能，遍历数据库中所有系统并建模",
    )
    parser.add_argument(
        "--include-root",
        action="store_true",
        help="全局建模时包含根节点(airplane)",
    )
    parser.add_argument(
        "--single-model",
        type=str,
        help="单次建模系统，无论是否存在系统都生成新模型（不存入数据库）",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="single_model_results",
        help="指定单次建模结果的输出目录",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="gpt",
        choices=["gpt", "claude", "dpsk", "qwen"],
        help="指定要使用的LLM提供商 (gpt, claude, dpsk, 或 qwen)",
    )

    args = parser.parse_args()

    # 未提供参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # 设置环境
    if args.setup:
        from auto_expansion_sysml.src.utils.setup import main as setup_main

        setup_main()

    # 初始化数据库
    if args.init_db:
        from auto_expansion_sysml.src.database.init_db import initialize_databases

        initialize_databases()

    # 全局自动建模
    if args.global_modeling:
        from auto_expansion_sysml.src.models.modeling_service import ModelingService

        service = ModelingService(provider=args.provider)
        try:
            logger.info(f"正在启动全局自动建模，使用提供商: {args.provider}...")
            # 根据include-root参数决定是否包含根节点
            exclude_root = not args.include_root

            result = service.global_auto_modeling(exclude_root=exclude_root)

            if result["status"] == "success":
                logger.info("全局自动建模完成")
                logger.info(f"处理的系统数量: {len(result['processed_systems'])}")
                logger.info(f"建模的子系统数量: {len(result['modeled_subsystems'])}")
                logger.info(
                    f"标记为小粒度的系统数量: {len(result['small_granularity_systems'])}"
                )
            else:
                logger.error(f"全局自动建模出错: {result['message']}")
        finally:
            service.close()

    # 建模系统
    if args.model:
        from auto_expansion_sysml.src.models.modeling_service import ModelingService

        service = ModelingService(provider=args.provider)
        try:
            logger.info(f"正在建模系统: {args.model}，使用提供商: {args.provider}")

            result = service.model_system(args.model, args.auto_expand)

            if result["status"] == "success":
                logger.info(f"成功建模系统: {args.model}")
                logger.info(f"系统ID: {result['system_id']}")
                logger.info(f"新系统: {result['is_new']}")
            else:
                logger.error(f"建模系统时出错: {result['message']}")
        finally:
            service.close()

    # 单次建模系统
    if args.single_model:
        from auto_expansion_sysml.src.models.modeling_service import ModelingService

        service = ModelingService(provider=args.provider)
        try:
            logger.info(
                f"正在单次建模系统: {args.single_model}，使用提供商: {args.provider}"
            )

            result = service.model_system_single(args.single_model)

            if result["status"] == "success":
                logger.info(f"成功单次建模系统: {args.single_model}")
                logger.info(f"系统ID: {result['system_id']}")
                if result["reference_system"]:
                    logger.info(f"参考系统: {result['reference_system']}")
                if result["parent_system"]:
                    logger.info(f"父系统: {result['parent_system']}")

                # 创建输出目录（如果不存在）
                output_dir = args.output_dir
                os.makedirs(output_dir, exist_ok=True)

                # 使用时间戳和系统名称创建文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_system_name = (
                    result["system_id"].replace("/", "_").replace("\\", "_")
                )
                output_file = os.path.join(
                    output_dir, f"{safe_system_name}_{timestamp}_{args.provider}.json"
                )

                # 将结果保存到JSON文件
                with open(output_file, "w", encoding="utf-8") as f:
                    # 确保所有内容都是JSON序列化的，包括嵌套的specification和model
                    json_result = {
                        "system_id": result["system_id"],
                        "system_name": args.single_model,
                        "specification": result["specification"],
                        "model": result["model"],
                        "reference_system": result["reference_system"],
                        "parent_system": result["parent_system"],
                        "timestamp": timestamp,
                        "provider": args.provider,
                    }
                    json.dump(json_result, f, ensure_ascii=False, indent=2)

                logger.info(f"结果已保存到: {output_file}")
            else:
                logger.error(f"单次建模系统时出错: {result['message']}")
        finally:
            service.close()


if __name__ == "__main__":
    main()

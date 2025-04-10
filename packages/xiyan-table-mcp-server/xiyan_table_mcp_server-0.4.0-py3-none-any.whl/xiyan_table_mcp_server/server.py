import logging
import os
import yaml
import pandas as pd
from mcp.server import FastMCP
from typing import Any, Dict, List
from .utils.prompt import USER_PROMPT
from .utils.common_utils import convert_csv_to_str
from .utils.llm_utils import call_openai_sdk

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("xiyan_table_mcp_server")

mcp = FastMCP("xiyan_table")

def get_yml_config(config_path: str = "config_demo.yml") -> Dict[str, Any]:
    """加载YAML配置文件
    
    Args:
        config_path: 配置文件路径
    Returns:
        Dict[str, Any]: 配置信息字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        logger.error(f"配置文件 {config_path} 未找到")
        raise
    except yaml.YAMLError as exc:
        logger.error(f"解析配置文件 {config_path} 出错: {exc}")
        raise

def load_data(config: Dict[str, Any]) -> pd.DataFrame:
    """加载CSV数据
    
    Args:
        config: 配置信息
    Returns:
        pd.DataFrame: 加载的数据表
    """
    try:
        return pd.read_csv(
            config["table"]["path"],
            encoding=config["table"]["encoding"]
        )
    except Exception as e:
        logger.error(f"加载数据文件失败: {str(e)}")
        raise

# 全局配置和数据
global_config = get_yml_config()
global_data = load_data(global_config)

# @mcp.resource(global_config["table"]["path"])
# def get_table_preview() -> Dict[str, Any]:
#     """获取表格预览数据"""
#     try:
#         preview_rows = global_config["table"]["preview_rows"]
#         preview_data = global_data.head(preview_rows)
#         return {
#             "columns": preview_data.columns.tolist(),
#             "data": preview_data.values.tolist(),
#             "total_rows": len(global_data),
#             "preview_rows": preview_rows
#         }
#     except Exception as e:
#         logger.error(f"生成表格预览失败: {str(e)}")
#         raise

@mcp.tool()
async def get_data(question: str) -> str:
    """查询表格数据
    
    Args:
        question: 用自然语言描述的查询问题
    Returns:
        str: 查询结果
    """
    try:
        prompt = USER_PROMPT.format(table=convert_csv_to_str(global_config["table"]["path"]), question=question)
        
        response = call_openai_sdk(
            key=global_config["model"]["api_key"],
            url=global_config["model"]["api_base"],
            model=global_config["model"]["model_name"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=global_config["model"]["temperature"]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"查询处理失败: {str(e)}")
        return f"查询过程中发生错误: {str(e)}"

def main():
    try:
        logger.info("启动MCP服务器")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"程序运行失败: {str(e)}")
        raise

if __name__ == "__main__":
    main()
import argparse

class ArgumentUtils:
    """
    命令行解析器类，用于解析命令行参数
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='书籍翻译')
        self.parser.add_argument('--config', type=str, default='config.yaml', help='配置文件路径')
        self.parser.add_argument(
            "--model_type",
            type=str,
            default="deepseek",
            choices=["deepseek", "openai"],
            help="模型类型，仅支持 deepseek / openai"
        )

        # --pages 翻译页数
        self.parser.add_argument(
            "--pages",
            type=int,
            help="需要翻译的页数，不填则翻译全本"
        )

        # --model_name 模型名称
        self.parser.add_argument(
            "--model_name",
            type=str,
            help="大模型名称（必填），例如 deepseek-chat"
        )

        # --input_file 输入文件
        self.parser.add_argument(
            "--input_file",
            type=str,
            help="需要翻译的书籍文件路径（必填）"
        )

        # --file_format 输出格式
        self.parser.add_argument(
            "--file_format",
            type=str,
            help="输出文件格式（必填），例如 epub / pdf / txt"
        )

        # --source_language 源语言
        self.parser.add_argument(
            "--source_language",
            type=str,
            help="原始语言（必填），例如 English"
        )

        # --target_language 目标语言
        self.parser.add_argument(
            "--target_language",
            type=str,
            help="翻译目标语言（必填），例如 Chinese"
        )

    def parse_args(self):
        """
        解析命令行参数
        :return: 解析后的参数对象
        """
        return self.parser.parse_args()



if __name__ == '__main__':
    arg = ArgumentUtils()
    print(arg.parse_args())

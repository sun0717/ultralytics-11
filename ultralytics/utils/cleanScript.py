"""
Summary: 指定要清除的字符串
"""
def remove_strings_from_file(file_path, strings_to_remove):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 删除列表中的所有字符串
        for string in strings_to_remove:
            content = content.replace(string, '')
        
        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"所有指定的字符串已从文件中删除。")
        
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到。")
    except Exception as e:
        print(f"处理文件时发生错误: {e}")

if __name__ == "__main__":
    # file_path = sys.argv[1]
    file_path = 'D://Code//ChangChun//ultralytics-11//ultralytics//utils//xx.yaml'
    # strings_to_remove = sys.argv[2:]
    strings_to_remove = [
        '<span class="token comment">',
        '<span class="token key atrule">',
        '</span>',
        '<span class="token punctuation">',
        '<span class="token number">',
        '<span class="token boolean important">',
        '<span class="token string">'
    ]
    remove_strings_from_file(file_path, strings_to_remove)
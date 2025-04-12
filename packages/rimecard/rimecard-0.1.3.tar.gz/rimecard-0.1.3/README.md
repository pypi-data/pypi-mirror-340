# rimecard

Extract vcf vcard contacts to rime pinyin dictionary.

将vcf格式的vcard通讯录里的姓名转换为rime输入法使用的字典格式。

将FN字段中的姓名合并，翻译为拼音，权重提升为1。


## 安装

`pip install rimecard`


## 使用

- `-i`定义输入文件
- `-o`定义输出文件，未定义时屏幕输出
- `-e`定义输出编码（默认utf-8）
- `-l`定义字符数限制（默认3）

`python3 -m rimecard -i vcard.vcf *.vcf [-o OUTPUT] [-e ENCODING] [-l WORDS_LIMIT]`


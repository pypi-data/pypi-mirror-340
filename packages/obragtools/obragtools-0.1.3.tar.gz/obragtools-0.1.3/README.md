# obragtools
一个将第三方包导入到基层笔记
实践级别

#### 本工具的主要目标是让大模型可以丝滑的使用和理解第三方的工具包
这是一个偏项目级别的工具包了
我们大致的思路是: 大模型可以达到理解并使用第三方包的程度
而我们开发的私有包则通过标准化和规范化,进而使大模型理解

在大模型可以完美使用一个三方包时, 可以开始拓展到多个包的配合使用
框架级别的包的使用等.为最终的调度赋能.

## 常规操作

### 导出环境
```
uv export --format requirements-txt > requirements.txt
```
### 更新文档
```
mkdocs serve # 预览
mkdocs gh-deploy -d ../.temp # 同步到github网站
```

### 发布
```
uv build
uv publish
```

### 运行测试并同步到测试服务
```
bash run_test.sh
```



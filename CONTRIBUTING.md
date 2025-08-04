# 贡献指南 Contributing Guide

感谢您对华语影视演员合作网络数据项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题 Reporting Issues
如果您发现了bug或有功能建议，请：

1. 在提交新issue前先搜索现有的issues
2. 使用清晰、描述性的标题
3. 提供详细的问题描述
4. 包含重现步骤（如果是bug）
5. 提供您的环境信息（Python版本、操作系统等）

### 提交代码 Submitting Code

#### 开发环境设置
1. Fork本项目到您的GitHub账户
2. 克隆您的fork：
   ```bash
   git clone https://github.com/yourusername/chinese-cast-network.git
   cd chinese-cast-network
   ```

3. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate     # Windows
   ```

4. 安装依赖：
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

5. 创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### 代码规范
- 使用Python 3.8+
- 遵循PEP 8代码风格
- 为新功能添加测试
- 保持向后兼容性
- 添加适当的文档字符串

#### 提交流程
1. 确保所有测试通过：
   ```bash
   python -m pytest tests/
   ```

2. 更新相关文档
3. 提交您的更改：
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

4. 推送到您的fork：
   ```bash
   git push origin feature/your-feature-name
   ```

5. 创建Pull Request

## 📝 代码风格

### Python代码规范
- 使用4个空格缩进
- 行长度不超过88字符
- 类名使用PascalCase
- 函数和变量名使用snake_case
- 常量使用UPPER_SNAKE_CASE

### 提交信息规范
使用以下格式：
```
type(scope): description

[optional body]

[optional footer]
```

类型 (type)：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(network): 添加多演员网络构建功能

- 支持同时分析多个演员的合作网络
- 添加网络合并算法
- 更新相关测试用例
```

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试文件
python -m pytest tests/test_data_loader.py

# 运行测试并生成覆盖率报告
python -m pytest tests/ --cov=src
```

### 添加测试
- 为新功能添加单元测试
- 测试文件命名：`test_<module_name>.py`
- 测试函数命名：`test_<function_name>`
- 使用pytest框架

## 📖 文档

### 更新文档
- 更新README.md中的相关部分
- 为新功能添加示例代码
- 更新API文档
- 在CHANGELOG.md中记录更改

### 文档风格
- 使用中英文双语（重要内容）
- 提供清晰的代码示例
- 包含必要的截图或图表

## 🏷️ 版本发布

项目使用[语义化版本](https://semver.org/)：
- **MAJOR**: 不兼容的API更改
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的bug修复

## 🎯 贡献方向

我们特别欢迎以下方面的贡献：

### 优先级高 High Priority
- 🐛 Bug修复
- 📊 性能优化
- 🧪 测试覆盖率提升
- 📖 文档改进

### 功能增强 Feature Enhancements
- 🎨 新的可视化样式
- 📈 更多网络分析指标
- 🔍 高级搜索功能
- 💾 数据导入/导出格式支持

### 长期目标 Long-term Goals
- 🌐 Web界面
- 🗄️ 数据库集成
- ⚡ 实时数据处理
- 🤖 机器学习集成

## 📞 联系方式

如果您有任何问题，可以通过以下方式联系我们：

- 提交GitHub Issue
- 发送邮件至：[your.email@example.com]
- 加入讨论：[项目讨论区链接]

## 📄 许可证

通过贡献代码，您同意您的贡献将按照项目的MIT许可证进行授权。

---

再次感谢您的贡献！🎉

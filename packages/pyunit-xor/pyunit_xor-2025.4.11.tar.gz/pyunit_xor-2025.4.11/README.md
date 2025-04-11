## XOR

一个简单的异或生成Token

## 安装
```
pip install pyunit-xor
```

## 使用
```python
from pyunit_xor import SimpleXOR

# 测试代码
if __name__ == "__main__":
    manager = SimpleXOR()
    tokens = manager.generate("2024-01-10 00:00:00")
    print("生成的Token:", tokens)

    # 验证Token
    is_valid, result = manager.validate(tokens)
    if is_valid:
        print("Token有效，过期日期:", result)
    else:
        print("Token无效，原因:", result)

```
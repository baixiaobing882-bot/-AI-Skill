# 倪海厦易经断事 AI Skill

一个面向 Codex 等兼容 Agent Skill 环境的、可复现的易经起卦与决策反思工具。它支持三枚钱币法、直接输入六爻和经用户同意后的机器随机模拟，并自动计算本卦、动爻、之卦、互卦、错卦与综卦。

> **非官方声明**：本项目为独立开发项目，不是倪海厦老师、其继承人或相关机构的官方产品，也未获得其授权或背书。项目不包含倪海厦课程原文、讲义、截图、视频、音频或专有断语。“倪海厦”一词仅用于描述用户期待的重时位、重验证、重行动的分析取向。

## 主要特点

- 原始投掷和六爻顺序可记录、可复算。
- 自动校验本卦、之卦、互卦、错卦和综卦。
- 清楚区分排卦事实、传统通用象义、情境推断和行动建议。
- 不作确定性预言，不冒充真实人物或官方传承。
- 对医疗、法律、投资和生命安全问题设置明确边界。
- 代码、说明和模板采用 MIT License；第三方仓库内容没有被复制进入本项目。

## 安装

### 方法一：让 Codex 从 GitHub 安装

把下面这段话发送给 Codex：

```text
请从这个 GitHub 仓库安装 Skill：
https://github.com/baixiaobing882-bot/-AI-Skill
```

### 方法二：下载 ZIP

下载仓库根目录的 `nihaisha-iching-divination.zip`，解压后把完整文件夹放到：

```text
~/.codex/skills/nihaisha-iching-divination/
```

确认以下文件直接存在，不要多套一层同名目录：

```text
~/.codex/skills/nihaisha-iching-divination/SKILL.md
```

安装后重启 Codex，使 Skill 元数据重新加载。

## 直接调用

Skill 名称：

```text
$nihaisha-iching-divination
```

### AI 模拟三枚钱币

```text
使用 $nihaisha-iching-divination 为我正式起卦。

问题：未来三个月，我是否应该接受现在这个工作机会？
重点：分析机会、风险、行动条件和止损线。
我同意使用机器随机模拟三枚钱币起卦。
```

### 自己投掷三枚钱币

本 Skill 约定正面 `H=3`、反面 `T=2`。连续投掷六次，第一次为初爻，之后自下而上记录：

```text
使用 $nihaisha-iching-divination 正式排卦并断事。

问题：我是否适合在今年内启动这个创业项目？
时间范围：未来六个月。
六次三币结果，自初爻到上爻依次为：

HHT
TTT
HHH
HHT
TTH
HTH

请先展示排卦事实，再分析卦象，最后给出可验证的行动建议、触发条件和止损线。
```

### 直接输入六爻

```text
使用 $nihaisha-iching-divination 起卦。

问题：未来三个月这个合作是否值得继续？
六爻自下而上：7、8、9、7、6、8。

请核对本卦、动爻、之卦、互卦、错卦和综卦，并进行审慎断事。
```

其中 `6` 为老阴、`9` 为老阳，二者属于动爻。

## 本地运行排卦器

```bash
python3 scripts/cast_hexagram.py \
  --question "是否接受 A 岗位" \
  --coins HHT TTT HHH HHT TTH HTH \
  --format markdown
```

运行测试：

```bash
python3 scripts/test_cast_hexagram.py
```

测试覆盖已知乾坤样例、三币计分、动爻翻转、错误输入，以及全部 64 种六爻结构的唯一映射。

## 目录结构

```text
├── README.md
├── SKILL.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── assets/
│   └── divination-report-template.md
├── references/
│   ├── casting-protocol.md
│   ├── hexagram-basics.md
│   ├── interpretation-framework.md
│   └── provenance-and-license-audit.md
└── scripts/
    ├── cast_hexagram.py
    └── test_cast_hexagram.py
```

## 版权与来源

本项目的脚本、模板和说明为独立编写，采用 [MIT License](LICENSE)。两个参考仓库均未发现标准开源许可证，因此本项目没有复制其代码、课程截图、转写、讲义、案例或独特断语。完整判断见 [来源、许可证与内容处置审计](references/provenance-and-license-audit.md)。

## 使用边界

本项目用于文化学习、反思和决策辅助。卦象不能证明因果、认定事实或保证未来结果，不应替代医疗、法律、投资、安全或其他专业判断。如存在现实紧急危险，请优先联系当地紧急服务或合格专业人士。

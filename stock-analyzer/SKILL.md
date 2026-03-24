---
name: stock-analyzer
description: Multi-agent stock analysis assistant using TradingAgents logic. Analyzes stocks by visiting 10jqka (TongHuaShun) directly via browser, no API keys needed. Provides fundamental, technical, and sentiment analysis through AI agents.
---

# Stock Analyzer

基于 TradingAgents 多智能体逻辑的股票分析助手。通过浏览器直接访问同花顺获取实时数据，无需 API Key，使用大模型进行基本面、技术面、情绪面综合分析。

## Core Capabilities

### 1. 多智能体分析框架

模拟 TradingAgents 的角色分工：

| 角色 | 职责 | 分析维度 |
|------|------|----------|
| **基本面分析师** | 财务指标、估值分析 | PE/PB/ROE/营收增长 |
| **技术面分析师** | K线形态、技术指标 | MACD/KDJ/均线/成交量 |
| **情绪面分析师** | 资金流向、市场情绪 | 主力净流入/换手率/龙虎榜 |
| **研究员(多空)** | 辩论评估 | 看多 vs 看空观点碰撞 |
| **风控经理** | 风险评估 | 止损位/仓位建议 |

### 2. 数据获取（浏览器自动化）

**数据源：同花顺 (10jqka.com.cn)**

**访问路径：**
```
股票详情页: https://basic.10jqka.com.cn/{stock_code}/
资金流向: https://basic.10jqka.com.cn/{stock_code}/captial.html
财务数据: https://basic.10jqka.com.cn/{stock_code}/finance.html
个股研报: https://basic.10jqka.com.cn/{stock_code}/report.html
```

**数据提取：**
- 使用 `browser` 工具访问页面
- 使用 `snapshot` 提取文本数据
- 解析关键财务和技术指标

### 3. 分析流程

```
用户请求 → 获取股票代码 → 访问同花顺 → 提取数据 → 
多智能体分析 → 综合报告 → 投资建议
```

**Step 1: 数据获取**
```python
# 访问同花顺个股页面
browser open https://basic.10jqka.com.cn/000001/
browser snapshot  # 提取页面数据
```

**Step 2: 多智能体分析**
将提取的数据分别喂给不同角色的 AI Agent：

1. **基本面 Agent**: 分析盈利能力、成长性、估值水平
2. **技术面 Agent**: 分析趋势、支撑阻力、买卖信号
3. **情绪面 Agent**: 分析资金流向、市场情绪、主力动向

**Step 3: 多空辩论**
- 多头研究员：列出看涨理由
- 空头研究员：列出看跌理由
- 交易员：综合观点，给出交易建议

**Step 4: 风控评估**
- 风险评估：波动率、流动性、黑天鹅风险
- 建议仓位：根据风险等级给出仓位建议
- 止损位：技术面止损点

### 4. 输出格式

**分析报告结构：**

```markdown
# {股票名称} ({代码}) 分析报告
生成时间: {timestamp}

## 📊 数据概览
- 当前价格: ¥xx.xx
- 涨跌幅: +x.xx%
- 市值: xxx亿

## 🤖 智能体分析

### 基本面分析师观点
{财务分析结论}
**评分**: x/10

### 技术面分析师观点
{技术形态分析}
**评分**: x/10

### 情绪面分析师观点
{资金流向分析}
**评分**: x/10

### 多空辩论
**多头观点**: ...
**空头观点**: ...

## 🎯 综合建议
- **操作**: 买入/持有/观望/卖出
- **目标价**: ¥xx.xx (+x%)
- **止损位**: ¥xx.xx (-x%)
- **建议仓位**: x%

## ⚠️ 风险提示
{风险说明}
```

## Usage Examples

### 分析单只股票
```
User: "分析一下贵州茅台"
→ 识别代码: 600519
→ 访问同花顺获取数据
→ 多智能体分析
→ 输出完整报告
```

### 快速技术诊断
```
User: "看看宁德时代的技术面"
→ 访问同花顺
→ 专注技术面分析
→ 给出支撑阻力位
```

### 对比分析
```
User: "对比分析一下比亚迪和特斯拉"
→ 分别获取两只股票数据
→ 并行分析
→ 对比输出
```

## 技术实现

### 核心脚本

**主分析流程**: `analyze_stock(stock_name_or_code)`

```python
def analyze_stock(query: str) -> dict:
    """
    分析股票主函数
    
    Args:
        query: 股票名称或代码
        
    Returns:
        包含完整分析结果的字典
    """
    # 1. 解析股票代码
    code = resolve_stock_code(query)
    
    # 2. 获取数据
    data = fetch_ths_data(code)
    
    # 3. 多智能体分析
    analysis = {
        'fundamental': fundamental_agent(data),
        'technical': technical_agent(data),
        'sentiment': sentiment_agent(data),
        'bull_bear': debate_agent(analysis),
        'risk': risk_agent(analysis)
    }
    
    # 4. 生成报告
    return generate_report(analysis)
```

### 数据获取函数

**同花顺数据提取**:
```python
def fetch_ths_data(stock_code: str) -> dict:
    """从同花顺获取股票数据"""
    base_url = f"https://basic.10jqka.com.cn/{stock_code}/"
    
    # 访问页面
    browser open base_url
    snapshot = browser snapshot
    
    # 解析数据
    data = {
        'price': extract_price(snapshot),
        'pe': extract_pe(snapshot),
        'pb': extract_pb(snapshot),
        'kline': extract_kline(snapshot),
        'fund_flow': extract_fund_flow(snapshot)
    }
    
    return data
```

### 智能体提示词模板

**基本面分析师提示词**:
```
你是一位专业的基本面分析师。请基于以下财务数据进行分析：

{fundamental_data}

分析维度：
1. 盈利能力（ROE、净利率）
2. 成长性（营收增长、利润增长）
3. 估值水平（PE/PB 分位）
4. 财务健康度（负债率、现金流）

输出：
- 分析结论（100字以内）
- 评分（1-10分）
- 关键风险点
```

**技术面分析师提示词**:
```
你是一位专业的技术分析专家。请基于以下技术数据进行分析：

{technical_data}

分析维度：
1. 趋势判断（均线排列）
2. 支撑阻力位
3. 技术指标信号（MACD、KDJ）
4. 成交量分析

输出：
- 技术形态判断
- 关键价位（支撑/阻力）
- 操作建议
- 评分（1-10分）
```

## Important Limitations

⚠️ **免责声明**:
- 本工具仅供学习和研究使用
- 不构成任何投资建议
- 股市有风险，投资需谨慎
- 分析结果仅供参考，不构成买卖依据

⚠️ **数据限制**:
- 依赖同花顺网页数据，可能存在延迟
- 浏览器访问可能受反爬限制
- 数据准确性以同花顺为准

⚠️ **分析局限**:
- AI 分析存在幻觉可能
- 无法预测突发事件影响
- 历史表现不代表未来收益

## Quick Reference

| 任务 | 命令示例 |
|------|----------|
| 分析股票 | "分析一下 600519" |
| 技术面诊断 | "看看 000001 的技术面" |
| 基本面评估 | "茅台的基本面怎么样" |
| 资金流向 | "宁德时代的资金情况" |

## Related Skills

- `browser` - 浏览器自动化
- `web_fetch` - 网页内容获取
- `image` - 图表分析（可选）

## 数据来源

- **同花顺**: https://www.10jqka.com.cn/
- **个股详情页**: https://basic.10jqka.com.cn/{code}/

---

**创作灵感**: 基于 TauricResearch/TradingAgents 多智能体框架思想，结合同花顺实时数据，打造无需 API Key 的本地化股票分析工具。

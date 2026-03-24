---
name: stock-picker
description: Intelligent stock screening and picking assistant. Selects top 5 short-term (1-3 months) and long-term (6-12 months) potential stocks from 10jqka (TongHuaShun) data. Uses multi-factor analysis including technicals, fund flow, fundamentals, and sentiment.
---

# Stock Picker - 智能选股助手

基于同花顺数据，通过多因子模型选出短期（1-3月）和长期（6-12月）最具上涨潜力的股票。

## Core Capabilities

### 1. 短期潜力股筛选（1-3个月）

**选股逻辑 - 多因子模型：**

| 因子 | 权重 | 筛选标准 |
|------|------|----------|
| **资金流入** | 30% | 龙虎榜净买入、主力净流入前50 |
| **技术形态** | 25% | 突破形态、量价齐升、MACD金叉 |
| **情绪热度** | 20% | 涨停基因、换手率3-15%、市场人气 |
| **题材催化** | 15% | 当前热点概念、政策利好预期 |
| **筹码结构** | 10% | 股东人数减少、筹码趋于集中 |

**数据源：**
- 龙虎榜: https://data.10jqka.com.cn/market/lhbgg/
- 资金流向: https://basic.10jqka.com.cn/{code}/captial.html
- 涨停分析: https://www.iwencai.com/stockpick/

### 2. 长期潜力股筛选（6-12个月）

**选股逻辑 - 价值投资+成长：**

| 因子 | 权重 | 筛选标准 |
|------|------|----------|
| **基本面** | 30% | PE<30、PB<5、ROE>10%、负债率<60% |
| **成长性** | 25% | 营收增长>15%、净利润增长>20% |
| **估值修复** | 20% | 处于历史PE低位、行业对比低估 |
| **机构动向** | 15% | 北向资金增持、机构调研增加 |
| **行业景气** | 10% | 政策支持、行业周期向上 |

**数据源：**
- 财务数据: https://basic.10jqka.com.cn/{code}/finance.html
- 股东研究: https://basic.10jqka.com.cn/{code}/holder.html

### 3. 选股流程

```
Step 1: 获取候选池
   ↓
   - 短期: 近期龙虎榜个股 + 涨停股 + 热点概念股
   - 长期: 沪深300成分股 + 业绩预增股 + 低估值股

Step 2: 多维度打分
   ↓
   - 对每个因子进行评分（1-10分）
   - 按权重计算综合得分

Step 3: 筛选排序
   ↓
   - 短期: 按综合得分排序，选前5
   - 长期: 按综合得分排序，选前5

Step 4: 生成报告
   ↓
   - 个股分析 + 买入逻辑 + 风险提示
```

## Usage Examples

### 选出短期潜力股
```
User: "帮我选几只短期可能涨的股票"
→ 访问同花顺龙虎榜
→ 获取近期涨停股
→ 多因子打分
→ 输出Top 5
```

### 选出长期潜力股
```
User: "有什么适合长期投资的股票"
→ 筛选低估值+高成长标的
→ 分析基本面
→ 输出Top 5
```

### 完整选股报告
```
User: "给我一份选股报告"
→ 同时输出短期Top 5 + 长期Top 5
→ 附带详细逻辑和风险提示
```

## Stock Screening Criteria

### 短期选股标准（详细）

**必选项（满足至少3项）：**
- [ ] 近5日上过龙虎榜且净买入为正
- [ ] 近10日有涨停记录
- [ ] 换手率>3%且<20%（活跃但不过度）
- [ ] 当前热点概念（AI、机器人、新能源等）
- [ ] 技术形态突破（新高、平台突破）

**加分项：**
- 股东人数季度环比下降
- 机构专用席位买入
- 业绩预增或扭亏
- 市值50-500亿（弹性适中）

**排除项：**
- ST股、*ST股
- 近一年有财务造假记录
- 大股东持续减持
- 日均成交额<1亿（流动性差）

### 长期选股标准（详细）

**必选项（满足至少3项）：**
- [ ] PE(TTM) < 行业平均值
- [ ] ROE > 10%（连续3年）
- [ ] 营收复合增长 > 15%
- [ ] 净利润复合增长 > 15%
- [ ] 负债率 < 60%

**加分项：**
- 行业龙头或细分冠军
- 北向资金持续增持
- 分红稳定且股息率>2%
- 政策利好支持

**排除项：**
- 连续2年亏损
- 经营性现金流为负
- 大股东高比例质押
- 行业处于下行周期

## Data Sources

### 同花顺页面

| 数据类型 | URL | 说明 |
|----------|-----|------|
| 龙虎榜 | https://data.10jqka.com.cn/market/lhbgg/ | 资金流入排行 |
| 涨停分析 | https://www.iwencai.com/stockpick/ | 涨停股筛选 |
| 业绩快报 | https://basic.10jqka.com.cn/{code}/ | 财务数据 |
| 资金流向 | https://basic.10jqka.com.cn/{code}/captial.html | 主力动向 |
| 股东研究 | https://basic.10jqka.com.cn/{code}/holder.html | 筹码变化 |

### 辅助工具
- i问财选股: https://www.iwencai.com/stockpick/
- 同花顺热榜: https://basic.10jqka.com.cn/hotstock.html

## Output Format

### 短期潜力股报告

```markdown
# 📈 短期潜力股 Top 5（1-3个月）
筛选日期: {date}

## 🥇 No.1 {股票名称} ({代码})
**综合评分**: x/10

**入选理由**:
- ✅ 资金: 龙虎榜三日净买入x亿
- ✅ 技术: 突破前期平台，MACD金叉
- ✅ 情绪: 换手率x%，市场热度高
- ✅ 题材: {热点概念}

**买入逻辑**: {简述}
**目标涨幅**: +15%~25%
**止损位**: -8%
**风险提示**: {风险点}

---

[重复No.2-5...]

## 📊 短期选股统计
- 平均市值: xxx亿
- 平均PE: xx
- 平均换手率: x%
- 主要概念: {概念分布}
```

### 长期潜力股报告

```markdown
# 📊 长期潜力股 Top 5（6-12个月）
筛选日期: {date}

## 🥇 No.1 {股票名称} ({代码})
**综合评分**: x/10

**基本面**:
- PE: xx | PB: x.x | ROE: xx%
- 营收增长: +xx% | 净利润增长: +xx%

**入选理由**:
- ✅ 估值: 处于历史xx分位，低估
- ✅ 成长: {成长逻辑}
- ✅ 机构: {机构动向}
- ✅ 行业: {行业逻辑}

**买入逻辑**: {简述}
**目标涨幅**: +30%~50%
**止损位**: -15%
**风险提示**: {风险点}

---

[重复No.2-5...]
```

## Implementation

### 核心函数

```python
def pick_short_term_stocks() -> List[Dict]:
    """
    选出短期潜力股
    
    Returns:
        包含Top 5股票信息的列表
    """
    # 1. 获取候选池
    candidates = get_short_term_candidates()
    
    # 2. 多因子打分
    for stock in candidates:
        score = calculate_short_term_score(stock)
        stock['score'] = score
    
    # 3. 排序并返回Top 5
    return sorted(candidates, key=lambda x: x['score'], reverse=True)[:5]

def pick_long_term_stocks() -> List[Dict]:
    """
    选出长期潜力股
    """
    # 类似逻辑...
    pass

def calculate_short_term_score(stock: Dict) -> float:
    """
    计算短期综合得分
    
    因子权重:
    - 资金流入: 30%
    - 技术形态: 25%
    - 情绪热度: 20%
    - 题材催化: 15%
    - 筹码结构: 10%
    """
    score = (
        stock['fund_flow_score'] * 0.30 +
        stock['technical_score'] * 0.25 +
        stock['sentiment_score'] * 0.20 +
        stock['theme_score'] * 0.15 +
        stock['chip_score'] * 0.10
    )
    return score
```

### 数据获取

```python
def fetch_lhb_data() -> List[Dict]:
    """获取龙虎榜数据"""
    browser open https://data.10jqka.com.cn/market/lhbgg/
    snapshot = browser snapshot
    # 解析数据...
    return stocks

def fetch_limit_up_stocks() -> List[Dict]:
    """获取涨停股数据"""
    # 使用iwencai或同花顺热榜
    pass

def fetch_fund_flow(stock_code: str) -> Dict:
    """获取个股资金流向"""
    browser open https://basic.10jqka.com.cn/{stock_code}/captial.html
    # 解析数据...
    return data
```

## Important Limitations

⚠️ **免责声明**:
- 本工具仅供学习研究，不构成投资建议
- 股市有风险，投资需谨慎
- 选股结果基于公开数据和AI推理，存在不确定性
- 过往表现不代表未来收益

⚠️ **数据限制**:
- 依赖同花顺网页数据，可能有时效延迟
- 部分数据需要登录或权限
- 浏览器访问可能受反爬限制

⚠️ **选股局限**:
- 无法保证100%准确性
- 市场环境变化可能导致逻辑失效
- 建议结合自身判断使用

## Quick Reference

| 任务 | 示例命令 |
|------|----------|
| 短期选股 | "帮我选几只短线股" |
| 长期选股 | "有什么适合长期持有的股票" |
| 完整报告 | "给我一份选股报告" |
| 查看逻辑 | "解释一下选股标准" |

## Related Skills

- `stock-analyzer` - 个股深度分析
- `browser` - 网页数据获取
- `web_fetch` - 新闻资讯获取

---

**选股理念**: 短期重资金+情绪，长期重基本面+成长，知行合一，理性投资。

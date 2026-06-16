<div align="center">

# cbec-qualification-review

**跨境商品上架前的 AI 体检：先判断能不能卖、值不值得卖、上架前还缺什么。**

[English](./README.en.md)

[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Hackathon](https://img.shields.io/badge/International%20Food%20Expo%20Hackathon-2nd%20Place-gold.svg)](#)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![No dependencies](https://img.shields.io/badge/dependencies-none-green.svg)](./scripts/qualification_audit_schema.py)

国际食品展黑客松第二名项目，现已开源。

</div>

---

跨境上架最贵的错误，往往不是选品错了，而是**货已经备好，平台才告诉你资质不够、授权不覆盖、标签要改、类目不能卖**。

给它一个商品、目标市场、平台、包装标签、证书报告或品牌材料，它会把这些问题提前摊开：哪些能推进，哪些要补件，哪些应该停下来人工复核。

## 它解决的核心问题

- **上架前不确定**：这个品在 Amazon / TikTok Shop / Shopee / Temu / Lazada / AliExpress / Tmall Global 能不能卖？
- **平台卡审说不清**：到底缺品牌授权、检测报告、标签、证书，还是主体/地区/类目不匹配？
- **包装和宣称有风险**：正背标、成分、过敏原、警示、认证标识、责任方、语言和功效宣称哪里要改？
- **定价和物流没依据**：竞品是谁、价格带在哪、空运/海运/海外仓会不会吃掉利润？
- **团队审核口径不一致**：每个人都凭经验判断，补件话术、证据记录和复核链路难统一。

## 你能直接得到什么

| 你关心的事 | 它给你的结果 |
| --- | --- |
| 这个品要不要继续推 | go / caution / stop / unknown，以及最关键的风险 |
| 上架前还缺什么 | 平台、市场、类目、品牌、标签、证书、物流的缺口清单 |
| 平台为什么卡审 | 哪份材料缺、哪份过期、哪份主体/地区/类目/型号不匹配 |
| 包装要不要重做 | 标签、警示、成分、认证标识、本地化语言和宣称风险 |
| 价格怎么定 | 竞品分层、渠道价格带、包装卖点和差异化建议 |
| 怎么跟供应商/客户说 | 可直接发出的补件话术，说明材料、格式、签发方、有效期和适用范围 |
| 团队怎么复核 | 状态、证据、来源、缺口、结论和审计记录 |

## 先看结果

### 消费者与竞品信号

![消费者与竞品信号](./assets/demo-consumer-competitor-signals.png)

### 竞品价格与渠道洞察

![竞品价格与渠道洞察](./assets/demo-competitor-pricing-channels.png)

### 包装、配方与定价建议

![包装、配方与定价建议](./assets/demo-packaging-formula-pricing.png)

### 物流对比与预算

![物流对比与预算](./assets/demo-logistics-budget-eu.png)

### 美国零售货架概念

![美国零售货架概念](./assets/demo-retail-shelf-concept.png)

## 适合谁

- **跨境卖家 / 品牌方**：在打样、备货、投流前，先知道这个品是否值得继续。
- **选品和运营团队**：不只看销量和价格，把准入、包装、物流、合规成本一起纳入判断。
- **合规 / 资质审核团队**：把审核口径变成固定状态、证据表、缺口表和可复核记录。
- **服务商 / 代运营**：快速判断客户材料哪些能用、哪些必须重开，减少反复沟通。

## 覆盖范围

- 平台：Amazon、TikTok Shop、Shopee、Temu、Lazada、AliExpress、Tmall Global
- 市场 / 区域：US、EU / EEA、UK、Japan、China import、ASEAN / Southeast Asia
- 类目：food、cosmetics、supplements、electronics、household chemicals

规则来源连接到 Amazon Seller Central、TikTok Shop Seller Center、FDA、CBP、European Commission、FCC、CPSC、ASEAN、Singapore HSA、Malaysia NPRA、GOV.UK、MHLW、METI、GACC、SAMR、NMPA、WIPO、EUIPO、USPTO 等官方或权威入口。

## 为什么不是普通“建议”

- 先确认平台、国家、类目、业务模式、申请人角色、品牌/IP 和材料范围，再给判断。
- 申请人材料只算提交证据，不默认等于真实有效；关键事实需要官方来源、注册库、签发机构或平台政策确认。
- 每个风险都落到 severity、evidence、source、impact、required action，方便人工复核。
- 缺范围、缺材料、材料过期、授权不覆盖、疑似造假或官方来源冲突时，不会硬给通过，会输出补件、拒绝或人工升级。

## 它怎么判断

![跨境商品出海上架评估整体逻辑图](./assets/project-logic-diagram-zh.png)

<details>
<summary>结构化结论状态</summary>

| 状态 | 含义 |
| --- | --- |
| `approve` | 当前材料和核验结果支持推进。 |
| `conditional_approve` | 可以推进，但需要完成边界清楚的低/中风险补正。 |
| `request_more_info` | 关键信息或材料缺失，暂不能判断。 |
| `reject` | 已确认禁售、严重不合规、无权销售、材料失效且不可补正等问题。 |
| `escalate_human` | 疑似造假、制裁/出口管制、身份敏感、法律歧义或官方来源冲突。 |
| `not_applicable` | 请求范围不适用于给定平台、市场、类目或审核目的。 |

</details>

## 当前质量状态

这个项目已经具备来源覆盖、结构化输出和可回放样例：已索引规则都有来源入口，关键路径覆盖通过、补件、拒绝、人工升级、证书过期、授权范围不匹配、申请材料未外部核验等场景。

规则包成熟度仍保持 `seed`。它适合做上架前体检、材料初审、补件生成和内部审核辅助；正式执法、平台最终提交、法律判断或高风险类目决策，仍需要人工复核和最新官方确认。

## 安全与边界

本项目用于跨境电商商品出海评估、上架准备、资质审核、材料初审、补件生成和内部流程设计，不提供法律意见，也不替代平台、监管机构、认证机构或专业合规顾问的最终判断。

含身份证件、银行账户、个人联系方式、合同、营业执照编号等敏感信息时，应按 [`references/privacy-security.md`](./references/privacy-security.md) 做最小化展示、脱敏和审计记录。

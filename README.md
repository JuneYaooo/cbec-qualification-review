<div align="center">

# cbec-qualification-review

**面向跨境电商卖家、品牌、商品、证书与平台准入材料的可审计资质审核 Agent Skill。**

Claude Code / Codex / OpenClaw / Hermes 等支持 Skills 的 agent 均可使用。装进 agent 后，可以用自然语言审核商家入驻、类目准入、品牌授权、产品合规文件、证书有效性和平台补件材料，输出可追溯的通过、补件、拒绝或人工升级结论。

[![Skill](https://img.shields.io/badge/Agent-Skill-orange.svg)](./SKILL.md)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![No dependencies](https://img.shields.io/badge/dependencies-none-green.svg)](./scripts/qualification_audit_schema.py)

</div>

---

## 能做什么

- **商家/KYB 审核**：营业执照、税务登记、收款主体、受益人、店铺申请主体和服务商资质。
- **品牌/IP 审核**：商标证书、品牌授权书、分销协议、授权链、销售地区、平台/渠道范围和有效期。
- **商品/类目准入**：食品、保健品、化妆品、电子电器、家化等类目的准入材料、限制品和禁售风险。
- **证书/报告核验**：CE、FCC、COA、SDS/MSDS、ISO、HACCP、Halal、Organic、检测报告等文件的主体、范围、日期、签发方和产品匹配。
- **平台规则路由**：按 Amazon、TikTok Shop、Shopee、Temu、Lazada、AliExpress、Tmall Global 等平台生成审核清单。
- **补件与整改**：把缺失、过期、不一致或无法核验的材料转成申请人可读的补件话术。
- **结构化审计输出**：使用固定 JSON contract、证据表、来源层级、风险等级、决策状态和 audit log 支撑复核。

## 适合哪些场景

| 场景 | 适合程度 | 说明 |
| --- | --- | --- |
| 商家入驻材料初审 | 很适合 | 能把主体、平台、市场、类目、材料清单和缺口先梳理出来。 |
| 品牌授权链审核 | 很适合 | 重点检查授权方权限、被授权方、品牌、地区、平台、品类和有效期。 |
| 证书/检测报告形式审查 | 很适合 | 能识别过期、主体不一致、产品型号不匹配、签发方不明等问题。 |
| 平台类目准入 checklist | 适合 | 可用规则包生成初始清单，但最终要求必须查官方来源。 |
| 内部审核流程设计 | 适合 | 已提供数据模型、状态机、证据链和补件模板。 |
| 直接替代法务/合规最终意见 | 不适合 | 本 skill 是运营资质审核框架，不是法律意见或监管最终解释。 |

## 核心决策状态

skill 的最终结论固定为六类，便于系统集成和复核：

| 状态 | 含义 |
| --- | --- |
| `approve` | 关键要求已满足，无高风险阻断项。 |
| `conditional_approve` | 仅剩低/中风险、边界清楚且可补正的问题。 |
| `request_more_info` | 关键材料缺失、无法核验或范围不完整，暂不能判断。 |
| `reject` | 已确认严重不合规、禁售、无权销售、材料失效且不可补正等问题。 |
| `escalate_human` | 疑似造假、制裁/出口管制、身份敏感、法律歧义或官方来源冲突。 |
| `not_applicable` | 请求范围不适用于给定平台、市场、类目或审核目的。 |

## 架构设计

这个仓库按 Agent Skill 的渐进加载方式组织：入口保持轻量，细节按场景加载，规则和校验逻辑外置。

```text
cbec-qualification-review/
├── SKILL.md                         # skill 入口：触发条件、核心流程、硬规则、引用地图
├── agents/openai.yaml               # UI 展示元数据
├── references/                      # 审核方法、规则、模板和工程化说明
│   ├── audit-workflow.md            # 审核阶段和最小决策包
│   ├── document-taxonomy.md         # 文件分类、字段抽取和一致性检查
│   ├── platform-market-matrix.md    # 平台/市场/类目路由
│   ├── global-country-framework.md  # 国家/地区规则兜底框架
│   ├── decision-rules.md            # 严重性、阻断项和最终状态逻辑
│   ├── verification-playbook.md     # 官方来源、注册库和证书核验方法
│   ├── privacy-security.md          # PII/KYB/KYC 隐私处理
│   ├── report-templates.md          # Markdown 和 JSON 输出契约
│   ├── rulepack-governance.md       # 规则包维护、版本和成熟度治理
│   └── implementation-blueprint.md  # 产品化数据模型、API 和测试建议
├── data/rulepacks/                  # 可组合规则包
│   ├── index.json                   # 规则包索引与组合顺序
│   ├── global-baseline.json         # 全局兜底规则
│   ├── platform-*.json              # 平台规则覆盖层
│   └── category-*.json              # 类目规则覆盖层
├── scripts/
│   └── qualification_audit_schema.py # 无依赖 schema、checklist、rulepack、golden case 工具
└── cases/                           # 代表性 golden cases
```

规则包组合顺序由 [`data/rulepacks/index.json`](./data/rulepacks/index.json) 定义：

```text
global -> platform -> region -> country -> category
```

这意味着基础规则先提供兜底，平台、地区/国家和类目规则逐层叠加；当多个包定义同一个 `requirement_id` 时，后面的更高优先级规则覆盖前面的规则。

## 架构是否合理

总体是合理的，尤其适合作为“审核操作系统”而不是静态法规百科。

| 维度 | 判断 |
| --- | --- |
| Skill 入口 | 合理。`SKILL.md` 负责触发、路由、硬规则和引用地图，没有把所有法规细节塞进入口。 |
| 渐进加载 | 合理。`references/` 按审核阶段拆分，agent 只在需要时读取对应文件。 |
| 输出契约 | 合理。`report-templates.md` 是字段单一来源，脚本能校验 JSON，便于产品化。 |
| 规则治理 | 合理。rulepack 有成熟度、来源、freshness、组合顺序和贡献流程。 |
| 风险控制 | 合理。明确区分 T1-T5 来源，不把申请人材料当作外部事实，敏感数据要求脱敏。 |
| 自动化程度 | 中等。脚本能生成样例、checklist、规则包模板并做校验，但不负责 OCR、联网核验和真实 registry 查询。 |
| 当前规则覆盖 | 需要加强。现有平台包和类目包多为 `seed`，很多包暂未填入 requirements/sources。 |

当前最重要的边界是：这个 skill 已经有完整审核框架，但还不是可直接离线作最终结论的法规/平台规则库。对 Amazon、TikTok Shop、Shopee、Temu、Lazada、AliExpress、Tmall Global 等平台的现行要求，最终决策前仍必须查官方平台政策、监管机构或注册库，并记录 URL、来源层级和 checked date。

## 推荐改进方向

1. **补齐高频规则包**：优先把 Amazon US food、TikTok Shop SEA cosmetics、Temu electronics、Tmall Global food/cosmetics 等高频组合做成 `validated` 包。
2. **增加 country/region 包**：目前 `index.json` 规划了 country/region，但仓库中还没有成熟国家包。建议先做 US、EU、UK、Japan、China import。
3. **扩展 golden cases**：每个进入 `validated` 或 `production` 的规则包，至少配 3 个代表性 case，覆盖 approve、request_more_info、reject/escalate。
4. **加入官方来源刷新机制**：可以增加脚本记录 source freshness，定期标出过期来源和需要重新核验的规则。
5. **产品化时补 OCR/registry 层**：当前脚本不做文件解析和外部查询；如果接入实际系统，应单独建设 document extraction、source verification 和 human review queue。

## 安装

### Codex

```bash
mkdir -p ~/.codex/skills
cp -R /path/to/cbec-qualification-review ~/.codex/skills/cbec-qualification-review
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/cbec-qualification-review ~/.claude/skills/cbec-qualification-review
```

安装后重启对应 agent，让 skill 元数据重新加载。

## 使用示例

```text
用 cbec-qualification-review 帮我审核这个 Amazon US 食品类目入驻包，判断能否通过并列出补件项。
```

```text
用 cbec-qualification-review 检查这份品牌授权书是否覆盖 TikTok Shop 马来西亚站和护肤品类目。
```

```text
用 cbec-qualification-review 给 Temu 电子产品供应商准入设计一套审核 checklist。
```

```text
用 cbec-qualification-review 把这批营业执照、商标证书、COA、SDS 和检测报告整理成结构化审核 JSON。
```

```text
用 cbec-qualification-review 根据当前材料写一封申请人补件通知，语气要适合运营发给商家。
```

## 脚本用法

[`scripts/qualification_audit_schema.py`](./scripts/qualification_audit_schema.py) 不依赖第三方库，可直接运行。

生成样例审核 JSON：

```bash
python3 scripts/qualification_audit_schema.py sample
```

按平台、市场、类目生成初始 checklist：

```bash
python3 scripts/qualification_audit_schema.py checklist \
  --platform amazon \
  --market US \
  --category food
```

校验审核 JSON：

```bash
python3 scripts/qualification_audit_schema.py validate path/to/review.json
```

生成国家规则包模板：

```bash
python3 scripts/qualification_audit_schema.py rulepack-new \
  --country-code DE \
  --country-name Germany \
  > data/rulepacks/country-DE.json
```

校验规则包：

```bash
python3 scripts/qualification_audit_schema.py rulepack-validate data/rulepacks/global-baseline.json
```

用 golden case 检查输出：

```bash
python3 scripts/qualification_audit_schema.py case-check \
  cases/golden-expired-certificate.json \
  path/to/review.json
```

## 输出格式

面向人看的结果建议使用 [`references/report-templates.md`](./references/report-templates.md) 里的 Markdown memo：

- Decision
- Scope
- Requirement Coverage
- Findings
- Missing or Invalid Materials
- Evidence and Sources
- Applicant-Facing Supplement Request
- Internal Notes
- Disclaimer

系统集成建议使用同一文件里的 JSON contract，并用脚本校验字段、状态、证据引用和来源引用是否完整。

## 维护规则包

新增或更新规则包时建议遵循 [`references/rulepack-governance.md`](./references/rulepack-governance.md)：

1. 新建 rulepack。
2. 补充官方来源，优先 T1/T2。
3. 运行 `rulepack-validate`。
4. 更新 `data/rulepacks/index.json`。
5. 增加对应 golden case。
6. 标注成熟度：`seed`、`validated`、`production` 或 `stale`。

不要把未核验的卖家经验、社媒说法或服务商文章写成 authoritative rule。它们最多作为线索进入 `notes` 或 `gaps`。

## 安全与边界

本项目用于跨境电商资质审核、材料初审、补件生成和内部流程设计，不提供法律意见，也不替代平台、监管机构、认证机构或专业合规顾问的最终判断。

含身份证件、银行账户、个人联系方式、合同、营业执照编号等敏感信息时，应按 [`references/privacy-security.md`](./references/privacy-security.md) 做最小化展示、脱敏和审计记录。

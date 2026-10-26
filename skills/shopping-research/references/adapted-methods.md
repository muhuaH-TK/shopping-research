# 方法来源与采用边界

本技能由当前项目需求、用户确认和实际试跑反馈整理编写。下列第三方链接只作为方法参考，没有安装或运行其脚本，也不继承其服务、权限、依赖、推广转链或未知填分规则。2026-10-22已有详细检索报告；2026-10-23正式建立时复读购物助手和劳工参考入口，未将旧核查日期更新成全部来源均重新验证。没有下载第三方技能包或复制其可执行代码；不把外部许可声明当作本项目的许可授权。

| 方法来源 | 参考的思路 | 本技能的调整 |
|---|---|---|
| [AI购物决策助手](https://github.com/jade888jgj/ai_shopping_assistant_skill/blob/main/SKILL.md)、[shopping-compare](https://github.com/wangranm-a11y/shopping-compare-skill/blob/main/SKILL.md) | 先需求和产品、后渠道；实测、差评追评和证据附录 | 不强迫每项判冠军，投诉召回匹配型号批次，不绑定特定浏览器 |
| [easybuy](https://github.com/chen8696/easybuy-skill/blob/main/SKILL.md) | 软文、成本价值、溢价及宣传兑现 | 不使用无来源成本/毛利百分比；投入另核同期间原始财务披露，不要求每步确认 |
| [双休了么](https://github.com/fore-vip/skills/blob/main/fore-vip-shuangxiu/SKILL.md) | 双休、工时、补偿、争议及供应链的实际主体与信源 | 劳工作附加项，不采用固定候选配额、缺项补分或未检出争议奖励；证据完整度不以是否填分替代 |
| [durable-tech-buy](https://github.com/Sukai777/durable-tech-buy/blob/main/SKILL.md) | 硬条件、同价替代、可靠性、同SKU核价、长期成本 | 指标及成本随品类落地，不照搬数码配件、持有期或评分权重，缺项不编总额 |
| [shopping-aggregator](https://github.com/DaizeDong/shopping-aggregator/blob/main/skills/shopping-aggregator/SKILL.md) | 版本、卖家、库存、时间、优惠、费用及重点复核 | 使用当前可用工具，不引入私有账本、外部运行依赖或扩大结算权限 |

不采用[省柴柴的推广披露处理](https://github.com/marywbrown/shopping-price-compare/blob/main/references/agent-instructions.md)；本项目要求说明推广和返利关系。仅限接入店铺的导购也不能替代面向消费者的开放研究。

## 本项目独立确定的规则

以支持当次购买决策为终点，保持完整研究深度；每个独立需求默认3—5个主要候选，先检查解决方案差异。分数旁并列购买状态，核心证据不对称时不强排；缺关键资料先研究其他候选，确需用户介入再集中请求，允许有据结束及没有可购买推荐。这批要求来自2026-10-23完整追问后的明确确认。

逐款前置分数/状态、商城和红包入口及独立12项说明，七项权重35/20/15/10/10/5/5；开放品牌与渠道、跨品类安全及食品专项、标准明示、具体负面扣分去重、四类价格、实际替代读取和分项证据边界，均按当前入口与对应参考执行。被后续要求替换的历史格式不再作为规则。历史商品报告保留其采集日期和结论，不因正式建立技能追溯重评；本地文档的保留期限与经确认清理另按[文档生命周期规则](document-lifecycle.md)执行，不表示永久保存。

技能采用入口和按需参考文件；结构参照[OpenAI官方技能文档](https://learn.chatgpt.com/docs/build-skills)。发布、备份和验证记录保存在项目报告中，不将项目目录或聊天历史当运行依赖。

# 验证范围 / Validation scope

版本：1.3.0，试用版；记录日期：2026-10-30。规则实现、固定材料执行、真实取证和客户端触发分别记录。

## 公开可复现的结果

[五组材料](tests/README.md)全部虚构，原始输入与oracle分开保存。每组使用三个独立上下文，评者不读取oracle、其他输出或预期答案。实际后端和采样参数未暴露，不能称跨模型重复试验。

- **r1十五份已实际运行，未通过。** 存在分项/完整总分漂移、购买状态不一致及锚点/范围问题。[原机器检查](tests/runs/r1/machine-check.json)、[语义审查](tests/runs/r1/semantic-review.md)、全部原输出和[规则快照](tests/rule-snapshots/README.md)保留，不以均分掩盖。
- **r2为共享口径的事后尺度标定复测。** 已观察15/15；机器检查=passed，语义检查=failed，尚不计整体通过。 见[r2机器检查](tests/runs/r2/machine-check.json)及[r2语义检查](tests/runs/r2/semantic-check.json)。原始记录及验收阈值未改，规则及[共享卡](tests/calibration/r2/README.md)有明确版本和哈希；不是新题盲测、自由评分或新材料泛化已稳定的证明。

- **r3仅对受影响的F2做第二次、也是最后一次定向修订复测。** 实际3/3份；机器=passed，语义=failed。原始事实、规则与共享卡不变，增加比较方向/基准/分母的逐字读回核对。R2那份方向写反的原件保留，不回填成正确。其他四组结果以R2审查范围为限。 见[r3语义检查](tests/runs/r3/semantic-check.json)。

最终限定结果：共观察33份输出。r2的F1/F3/F4/F5在已知材料及共享尺度下通过机器和语义检查；F2最后r3仍有比较表述问题，未通过。已达到两次修订复测上限，不再追加；本版按部分验证的试用版交付，不能称固定评分测试全部通过。

容差：分项漂移≤1/10、完整总分漂移≤5/100；安全、状态、关键反证和扣分去重必须一致。部分分保留原项目/分母。算式和结构通过不代替语义复核。标准库检查器只检查实际文件，不调用模型、不生成缺失评分；轮次参数限结果目录内的r加正整数。

## 其他范围与限制

| 范围 | 实际观察及界限 |
|---|---|
| 运行结构 | 官方quick_validate已在任务隔离、哈希锁定校验组件支持下实际通过；技能本身没有增加运行依赖；相对引用及私人路径另作检查 |
| 输入版本 | 规则、原始材料及校准卡哈希分别在[rounds.json](tests/rounds.json)和快照保存；整个目录哈希不同于单SKILL.md哈希 |
| 文件交付 | 维护流程检查压缩包可打开、内容字节一致及本地安装；不推定其他客户端加载或触发成功 |
| 真实研究 | 候选r1完成内部取证、先初判后比稿及补查，研究仍有覆盖/证据缺口；最终r2未将全部真实取证重跑。题设、商品报告、来源及普通搜索对照不整理成公开案例 |
| 效果主张 | 未证明整体优于普通搜索、普遍省钱或保证完整购买结论；候选数、篇幅和低标价不单独证明价值 |
| 语言与客户端 | 代理中英输出有内部观察；实际客户端自动加载/触发未观察。文件存在、安装一致或双语文本不能代替客户端端到端验证 |

价格、库存、规范和版本只在实际来源及读取时间范围内成立；修改报告或技能不刷新它们。资料有效性独立于30天文档清理期限。固定测试不证明现实商品质量、安全、交易可执行性或实际购买效果。

## English

Version1.3.0 is a trial. Fifteen observed r1 outputs failed drift/status/rubric checks; original fictional facts, outputs, semantic findings and exact rule snapshots remain available. Observed 15/15; machine=passed, semantic=failed; no overall pass is claimed.

The r2 numerical checks passed, but semantic review found one reversed comparison in F2-A. The original is retained. A final targeted r3 rerun covers F2 only, adding explicit number/direction/denominator readback without changing raw facts, runtime or calibration. Its separate observed records, rather than a rewritten r2 output, determine that limited result.

There are 33 observed outputs. The r2 F1/F3/F4/F5 checks passed within known material and shared rubrics; F2 still failed the final r3 semantic review because of comparison wording. Both permitted repair rounds are exhausted. This is a partially verified trial, not a full fixed-test pass.

The r2 run is post-hoc calibration on known material using shared scoring cards. It is not blind generalization testing, proof of unconstrained scoring stability, statistical reliability or cross-model performance. Raw facts and acceptance tolerances remain unchanged. Unknown backend and sampling details remain unknown.

Structural checks, arithmetic, semantic review, file integrity, actual-client invocation, real evidence closure and purchase outcomes are separate claims. Real studies and comparisons stay internal. This release does not claim general superiority over ordinary search or proven savings. Actual-client automatic loading/triggering remains unobserved. Prices and other changing fields retain actual source dates.

# Houdini Development Log

## Project Overview

### 教室：真实世界 → 异化世界

更新时间：2026-11-26（北京时间；本次会话记录）。本文同时作为后续 Codex 的技术交接文档。

**最新组合基线：`E:/1126/1126.hip`。** 2026-11-26 已完整合入用户指定的 `tableright` 桌椅资产，保留正确教室；用户在实际打开结果后确认桌椅与教室形态非常接近理想效果。来源、逐节点档案、已运行脚本及防返工约束见[1126 合并成功记录](#baseline-1126-merged-20261126)。此前教室本体 40 帧导出及 SP／UE 成功保留为独立的[11 月 25 日历史记录](#room-uv-animation-20261125)，不是本次组合文件的新全段导出证据。

目标是在 Unreal Engine 中完成真实教室向异化教室转变的连续镜头。用户已经确定两张视觉参考：正常教室与同一空间的异化状态。后续模型、材质、动画、灯光、HDRI 和程序均服务于这两个目标画面。

- 保留已确定的主机位、构图与主要异化运动，不因 UV 修复随意重做布局。
- 用户计划于 **2026-11-27 投递**，优先完成镜头可见部分和可验证的成片。
- 用户确认 Houdini → Substance 3D Painter（SP）→ UE 的制作链已跑通；HDRI 已准备。
- AI＋Python 生成模型及处理破面已有可用流程。以上流程完成情况来自用户反馈，并非本文作者在 UE 中重新运行验证。

### 当前决策：两套独立资产

| 版本 | 数量与用途 | 当前要求 |
| --- | --- | --- |
| 正常世界静态版 | 5×5 桌子＋5×5 椅子，即 25 桌、25 椅 | 先完成静态网格及材质验证，不需要 Alembic |
| 异化世界动画版 | 保留已定构图与运动；历史版本为 25 桌、20 椅，椅子为构图改成 4×5 | 保持独立，确认代表帧后验证完整 40 帧 |

这是一项制作决策，**不表示两套最终资产均已制作、导出并验收**。

两套模型可以有不同拓扑，但切换处必须检查物体位置、姿态、数量、材质与光照连续性。镜头移动或遮挡可辅助衔接，不能保证数量差异天然不穿帮。蓝图触发／显隐切换逻辑留到资产与动画验证之后。

创建静态版时应隔离源分支，并检查参数中的绝对路径引用；复制节点不保证表达式引用也已独立。不要直接修改动画版的 Grid 来制作静态版。

<a id="baseline-1126-merged-20261126"></a>

## 2026-11-26：1126 桌椅与教室完整合并，用户确认接近理想效果

> **后续制作的最新组合基线：`E:/1126/1126.hip`。** 用户已实际打开该路径，在 Houdini 第 20 帧展示桌椅与教室同时存在的画面，明确评价为“第一次，非常接近完美的一个桌椅形态和教室形态”，并要求完整记住此次成功方法，避免回退与返工。
>
> **本节优先于下文旧版本的“当前基线／下一步”描述。** 旧 `1124`、`ROOM_DIRECT_UV_*` 和失败补丁仅作为历史、算法与诊断参考，不得在没有当前任务依据的情况下重新覆盖本基线。

### 1. 唯一工作文件与两个受保护的正确源

| 路径 | 本次身份 | 后续约束 |
| --- | --- | --- |
| `E:/1126/tableright.hip` | 用户指定的正确桌椅来源；实际取其整个 `/obj/other`，其中包含桌椅、书本／纸笔、UV 缓存及原动画 | 保持源文件不变；不得为了整理或修另一部分而覆盖 |
| `E:/1126/wallright.hip` | 用户指定的正确教室／墙来源 | 保持源文件不变；本次没有单独上传它，不声称读取过这份独立文件 |
| `E:/1126/1126.hip`，合并前 | 用户明确说明它是 `wallright.hip` 的直接复制；实际上传、读取并作为教室基底 | 本次唯一允许替换的正式工作文件 |
| **`E:/1126/1126.hip`，合并后** | **保留该基底的教室等全部其他内容，完整换入 `tableright` 的 `/obj/other`** | **以后在此组合基线上继续制作，按当次授权限制修改范围** |
| `E:/1126/_merge_rollback/1126.hip` | 脚本保留的一份合并前回退文件 | **不是合并结果，不要拿它查看成功状态或继续制作** |

上传的是 `1126.7z.001`～`.004` 和 `tableright.7z.001`～`.005`。必须按数字分卷顺序连接，再解压。用户新建 `E:/1126` 是为了结束此前的版本混乱；不得再次自动引用 `E:/1120` 下某个旧编号作为本次恢复源。

### 2. 本次真正做了什么

这是一次**保存完整桌椅资产的文件合并**，没有重新建立 UV 算法，没有按墙体算法重算椅子，也没有为通过检查而改变模型、动画、减面、细分或 UV 比例。

两份 HIP 都是可解析的 `070707` odc CPIO 归档。本次定义替换范围为：记录名以 `obj/other.` 或 `obj/other/` 开头。前者包含对象本身参数与网络信息，后者包含全部后代、接线、关键帧、缓存和显示／渲染标记；不能误匹配 `other2` 等其他对象。

1. 对上传文件计算完整 SHA-256，确认版本与分卷解压结果。
2. 核对跨资产依赖：`tableright` 的所有材质记录在基底中均存在且逐字节相同；所引用的 `/obj/cam1` 内容相同；内嵌节点定义的内容相容，差异涉及容器日期／索引元数据。没有新增外部资源依赖。
3. 完整移植 `/obj/other` 的归档记录，包含 `UV_VERIFIED_REFERENCE_1124` 的实际 Stash 几何。保留原归档的两个依赖加载区块位置，不把所有子节点任意挤到文件头。
4. 除这一范围外，所有记录都使用合并前 `1126` 的原始字节；`classroom_generator`、`geo1`、摄像机、材质、场景设置和其他对象未被替换。
5. 在临时文件中完成写入，核对整个结果哈希及逐条记录来源，原输入文件哈希保持不变；独立使用 libarchive 验证归档可读，再生成成品压缩包并通过解压 CRC 校验。
6. 给用户的独立本地脚本也用实际上传文件运行过，生成相同结果；重复运行识别已合并哈希后直接结束。代码只做文件读写与校验，不启动 UV 展开、全帧 cook 或导出。

**不能把本次固定字节范围当作通用 Houdini 合并 API。** 归档布局和脚本偏移仅对下面两份精确哈希的输入成立。不同 HIP、Houdini 重新保存后的文件或变化的节点定义，必须重新解析、核对边界和依赖；不能删除哈希检查来“强行继续”。需要原生节点操作时应使用适合该文件的 Houdini API，并重新验证保护范围。

### 3. 文件身份和实际验证结果

| 文件身份 | 字节数 | SHA-256 |
| --- | ---: | --- |
| 上传的 `1126.hip`，教室正确的基底 | 417,487,984 | `aa3c8d64c79c8e3e45dd095e6dc4b6215cfb30912df50c05a55cd0d5c5f7efa5` |
| 上传的 `tableright.hip`，桌椅正确的来源 | 540,938,171 | `fba1ccd9ab7e334ccca2c632ccd3613a3a20274893aa8aaa405b56be4af81835` |
| 离线生成的组合 `1126.hip` | 549,322,663 | `714d5ba42c2732807220de570ec520f671a30ca7b35837656d47c830ff491c80` |

- `/obj/other` 的 **1,966 条原始记录**与 `tableright` 一致；其余 **1,715 条记录（含归档结束标记）**与基底一致。
- 合并后共 **3,680 条内容记录**，另加一个结束标记。离线清点为 **762 个节点**：桌椅范围含根对象共 **429** 个，教室范围含根对象共 **274** 个，其余为材质、摄像机和其他网络。
- 本机分析没有运行 Houdini。原生打开及第 20 帧的最终画面由用户本机截图和明确反馈确认；此前 `3/3 完成` 只代表文件写入与校验通过。
- 这些哈希标记的是本次精确输入及离线生成文件。Houdini 正常保存可能改变时间戳、界面状态与归档字节，哈希变化本身不能证明 UV 损坏。

可复核档案位于 [`records/houdini/2026-11-26-1126-merge/`](records/houdini/2026-11-26-1126-merge/)：`manifest.json` 保存证据与范围，`node_snapshot.json` 保存逐节点类型、连接、标记和参数／关键帧记录指纹，`combine_local.py` 保存这次已经实际运行的独立脚本。档案不包含大型 HIP 或外部 FBX，不是完整资产备份；不能脱离精确源文件把它当成重建全部几何的输入。

### 4. 桌椅成功版本的关键实接线

以下连接直接读取自合并后的 HIP，不是根据节点名称推测：

```text
/obj/other/merge4（原动态桌椅模型）
  ↓ input 0
DESK_FINAL_UV_ON_ANIMATED_DESKS（Attribute Copy）
  ↑ input 1 = UV_VERIFIED_REFERENCE_1124（已保存几何的 Stash）
  ↓
DESK_FINAL_divide2 → DESK_FINAL_edit4
  ├─ DESK_FINAL_REDUCE_REST（Timeshift）
  ↓ input 0                     ↓ input 1
DESK_FINAL_polyreduce3
  ↓
DESK_FINAL_REPLACE_DESKS_ONLY ← DESK_FINAL_KEEP_ORIGINAL_BOOKS_AND_PENS
                               ↑ input 0 = merge1
  ├─ uvquickshade1（检查预览）
  └─ divide1 → polyreduce1 → clean1 → pack3 → rop_alembic1
```

书本／纸笔的保留分支直接来自 `merge1`，没有再次经过旧全场景 `attribcopy1` 的错误 UV 覆盖。这是需要持续保护的连接。`DESK_FINAL_REPLACE_DESKS_ONLY` 的 input 0 是保留书本／纸笔的结果，input 1 是修复桌椅的减面结果。

`UV_VERIFIED_REFERENCE_1124` 是真实的 Stash，几何保存于 `.parm` 的 `geometry:` 编码；其参数记录约 131.8 MB。没有同名 `.data` 不能据此说它没有缓存。旧 `DESK_FINAL_ORIGINAL_UV_LOCKED`、`DESK_FINAL_UV_LOCKED`、`WOOD_DENSITY_FIXED_UV`、`IRON_DENSITY_FIXED_UV`、`IRON_TINY_AREA_FIXED_UV` 也随完整网络保留，本次没有删除旧回退参考来压缩工程。

归档中仍有旧 `uvautoseam`、`uvflatten`、`uvlayout` 节点，不代表当前正式链必然每帧重新展开。先检查实际依赖、硬锁／缓存、显示与导出标记；不得按名称批量删除或仅因它们存在就改写成功主链。

### 5. 教室成功链继续保持原样

```text
/obj/classroom_generator/geo1/merge4
  ↓ input 0
ROOM_UV_ANIM_INPUT
  ↑ input 1 = ROOM_ALL_UV_20261124_234637_284042（Stash）
  ↓
ROOM_UV_TAG_AS_TEXTURE
  ↓ 原翻面检查／修正、transform6
subdivide1 → DETAIL_SUBDIVIDE_2 → normal1 → bend3
  ↓
merge14 → divide1 → divide2
                       ↑ input 1 = timeshift1
  ↓
polyreduce1 → clean4 → ROOM_UV_ANIM_MATERIALS → ROOM_UV_ANIM_OUT
  ├─ ROOM_UV_ANIM_CHECK
  └─ pack1 → rop_alembic1
```

这条主链及全部教室参数来自上传的合并前 `1126`，本次没有改接或重算教室。墙体“在低面数源建立正确静态 UV、保存后沿原细分与动画传递”的原理见下方 11 月 25 日记录；不能把那份历史记录的文件名再次当成覆盖当前教室的指令。

### 6. 仍需保留的外部资源与查看设置

桌椅网络保存的资源路径包括：

- `E:/small/Book_3_Books_Set1_0.FBX`
- `E:/small/stationery_supplies_pencil_new_b.FBX`
- `E:/uv_checker_dense.png`
- 摄像机避让脚本引用 `/obj/cam1` 和 `/obj/other`。

这些引用在两个输入中一致，本次没有改写或移走资源。迁移整套资产时仍要核对资源是否存在；不能声称 HIP 已嵌入全部 FBX 和纹理。

`uvquickshade1` 原参数中的 `texture_s = (1, 240, 1)` 连同其他参数完整沿用，并非本次新增的纹理缩放。历史 ROP 还保存了 `E:/1120/animation2` 和很短的导出范围；**本次没有执行新导出，也没有据此修改路径或帧段**。后续导出必须按用户当前镜头需求独立核实。

### 7. 文件已合并不等于窗口已加载：本次实际发生的误会

文件级脚本写入磁盘后，已打开的 Houdini 场景仍是旧的内存状态。用户第一次截图已显示 `3/3 完成`，但没有证据证明结果文件已重新加载；不能据旧视口继续运行另一个修复补丁。

随后用户实际打开了 `E:/1126/_merge_rollback/1126.hip`。标题栏清楚显示回退目录，视口仍有旧问题。备份与正式文件同名容易造成混淆，这是交付命名与说明应改进的地方，不能责怪用户，也不能把回退文件画面当成新合并失败的证据。

最后通过明确路径打开：

```python
import hou
hou.hipFile.load(r"E:/1126/1126.hip")
```

如有保存提示，放弃旧场景未保存状态，防止旧内存内容覆盖正式文件。用户随后展示正确标题栏并明确认可组合形态。以后必须确认 `hou.hipFile.path()` 的完整路径；同名文件仅看 basename 不足以确认版本。上传基底内部保存的 `HIPFILE`／`HIPNAME` 可能仍为 `wallright`，实际打开路径不能靠这些历史保存变量猜测。

未来若需要新备份，使用一个单独回退目录及清楚的 `BEFORE_...` 名称，给用户一个明确的正式工作路径；不要产生几十份顶层时间戳变体。**本次现存回退路径如表所列，不要为了整理擅自移动或删除用户文件。**

### 8. 后续操作约束与证据边界

1. 先读本节，再核对当前实际工程；将当前用户明确认可的组合基线视为起点，不以更旧版本或某个失败备份替代。
2. 用户已经确认正确的部分保持不动。桌子、椅子、书本、墙体分别限定修改范围；为修一部分而触碰其他部分，必须有当前任务的明确依据。
3. 合并正确资产时直接保留实际节点、参数、关键帧、UV 缓存、原动画、材质与外部引用，不做无关的全场景重投影、重新展开、减面或动画重建。
4. 几何映射确有必要时，先验证零件和逐面面角对应；不能只因点／面数量相等就按内部 vertex 数组盲拷贝，不以最近点碰运气。
5. 以缓存和静态参考减少重复 UV 运算。先做能解决具体问题的检查，不默认要求用户反复启动 Houdini、全帧强制 cook 或导出大型 ABC 来证明一个文件合并。
6. 失败时保护原工作文件；交付前用实际输入验证脚本、保护范围、依赖与重复运行行为。提供独立、可直接复制的 Shell 代码，不依赖旧 Shell 临时变量。
7. `DONE`、`3/3`、哈希、归档可读和一张预览截图属于不同层级的证据。直到实际打开和用户确认，不能把磁盘校验称为视觉验收。
8. 当前验收是用户对第 20 帧组合形态的明确正面反馈。**没有新增全 240 帧／完整片段、每个书本面和每条桌椅腿的 UV 质量自动验收，也没有本次合并后的 SP、UE 或 ABC 导出验收。** 下文教室历史 40 帧成功仍是历史事实，不能移作本次整套合并版本的新导出证据。
9. 当前截图的 `other` 仍有黄色警告图标；未读取具体警告文本，不推断其成因，不擅自改造已经得到用户认可的网络来消除图标。

本次只补充技术记忆与复核资料，未继续修改用户的 HIP、节点、UV 或动画。后续若用户指出具体缺陷，应以此基线做局部修复，并保留其余已认可部分。


<a id="room-uv-animation-20261125"></a>

## 2026-11-25：教室本体的正确 UV 接回原动画，完整导出成功

> **2026-11-25 当时的教室本体成功基线：`E:/1120/ROOM_DIRECT_UV_20261125_004415_787159.hip`。** 当前组合工作文件以[1126 成功记录](#baseline-1126-merged-20261126)为准。
>
> 本次处理的是 `/obj/classroom_generator/geo1`，不是 `/obj/other` 的桌椅修复。正确的静态 UV 已有，最终工作是把它按正确对应写入原动画网格，移除会覆盖它的旧 UV 处理。保留原细分、变形和动画控制，不复制另一套动画继续制作。

### 1. 已经确认的结果，以及证据范围

| 项目 | 本次结果／证据 |
| --- | --- |
| 正确源 UV | 已从用户上传 HIP 中解码两份 Stash 的实际几何；墙体为可辨认的大面、条带和门窗开口布局 |
| Houdini 中的动画附着 | 用户展示静止状态及第 46 帧扭曲状态，棋盘格随原教室动画变形；用户确认这次正确 |
| 整段导出 | 用户实测反馈：**共 40 帧，文件 4 GB 多，十多分钟导出完成** |
| SP | 用户已打开导出的教室；Texture Set 列表为 `ROOM_*` 分类，能看到输入 UV |
| UE | 用户最新截图显示带材质的墙、地板、窗帘、灯具等处于异化弯曲状态，并明确确认结果正确 |
| 自动材质脚本 | 后续另提供了 Painter 基础材质铺底试做代码；尚无该代码成功运行反馈，不作为本次 UV 成功的证据 |

这是一次实际完成导出并获得 SP／UE 画面反馈的结果。它不是“只创建了预览节点”或“只打印 DONE”。同时，**没有进行全 40 帧逐面零重叠、零越界、零拉伸的自动验收**；末端代码对越界角点只打印数量，不会因数量非零自动阻止导出。

40 是用户反馈的总帧数，不等于已核实导出范围必然为 `1–40`；最终起止帧、帧率及 ABC 精确文件名未回报。第 46 帧是预览证据，不能据此擅自把动画结束帧设为 46、48 或时间轴默认的 240。

分析侧读取、解包了 HIP、节点参数、关键帧与保存的几何，并测试了数据对应逻辑；没有在分析机器上启动 Houdini 21。实际 cook、导出、SP 和 UE 画面由用户本机运行与反馈确认。

### 2. 文件档案：哪些能作为基线，哪些已经废弃

| 文件／数据 | 用途与状态 |
| --- | --- |
| `E:/1120/1124.hip` | 最初工程之一；不要用新结果覆盖唯一原始工程 |
| `1124_BEFORE_EXPORT_CHECK_20261124_170931_622594.hip` | 本次教室导出、UV 排查的早期归档 |
| `E:/1120/ROOM_UV_SOURCE_20261124_225735.json` | 从 `merge4` 导出的低面数源诊断数据：点、逐面点序、UV、分组和部分属性 |
| `ROOM_UV_PREVIEW_20261124_233142_413254.hip` | 第一版已保存的低面数 UV／材质预览 |
| `ROOM_ALL_UV_PREVIEW_20261124_234637_284042.hip` | 扩展到整套教室材质分类的静态 UV 预览；不是动画导出结果 |
| `ROOM_UV_ANIMATION_20261125_000554_929626.hip` | 曾创建复制动画、携带 `uv_room_saved` 的分支；方案已废弃 |
| `ROOM_UV_INSET_20261125_001817_905972.hip` | 曾统一缩小 UV 以通过范围检查；单独墙体仍被传乱，**不是成功版本** |
| `ROOM_UV_INSET_20261125_001817_905972.7z.001`～`.004` | 用户重新上传的四分卷；实际重新读取了其中 HIP，不只根据截图猜测 |
| `ROOM_BEFORE_DIRECT_UV_20261125_004415_787159.hip` | 成功改接前的自动备份 |
| **`ROOM_DIRECT_UV_20261125_004415_787159.hip`** | **本次成功另存文件，原动画链直接使用正确 UV** |

四个分卷按文件名的 `.001 → .004` 顺序合并后解压。得到的失败现场 HIP 为 417,649,920 字节；不能按上传目录 UUID 排序合并分卷。离线读取到 3,783 条 HIP 归档记录。两份 Stash 的几何存放在 `.parm` 中的 `geometry:` 编码值，不能因为没有同名 `.data` 文件就判断它们没有保存几何。

成功工程内已保存正确 UV 的 Stash，以及实际使用的节点脚本。**日常打开、播放、导出不依赖旧 Python Shell 的临时变量或上述源 JSON。** 源 JSON 和旧工程仍应保留，供诊断与重建，不是每次打开成功工程都要重新读取的必需输入。

### 3. 工程实际长什么样

```text
/obj
├─ other
│  └─ 桌椅、书本、纸笔与此前 DESK_FINAL_* UV 修复
└─ classroom_generator
   └─ geo1
      ├─ 墙／地／顶、门窗、百叶、窗帘、灯具、空调、暖气
      ├─ 黑板、公告板、书架、书本纸张、管线等生成分支
      ├─ merge4                         # 教室本体源合并，含多类物体
      ├─ 原翻面修正、细分、法线、bend3 动画与后处理
      ├─ ROOM_UV_SOURCE_PREVIEW         # 已保存的第一份正确静态 UV
      └─ ROOM_ALL_UV_20261124_234637_284042
                                         # 最终采用的整套正确 UV 源 Stash
```

两个网络都有 `merge4`、`polyreduce1` 等常见名称。脚本必须使用完整路径，不能将教室修复误接到桌椅网络。

从重新上传的 HIP 中读出的正确参考几何：

| 点数 | 面数 | 面角／vertex 数 | UV |
| ---: | ---: | ---: | --- |
| 14,780 | 20,443 | 72,611 | vertex `uv`，每个面角 3 个 float 分量 |

其中 `ROOM_Walls` 对应 245 个源面。这个数量仅是低面数参考；最终模型经过细分、三角化与减面后面数会增加，不能因最终墙体不是 245 面就判定模型被重复生成。

#### 两级细分是原造型／动画的一部分

实际读取版本包含：

```text
subdivide1
  algorithm = osdbilinear
  iterations = 3
  group = * ^WIRE_FITTING ^TIED_CURTAIN_CLOTH ^TIED_CURTAIN_BAND
          ^MAT_PAPER ^MAT_BOOK_COVER ^Ceiling ^Heater

DETAIL_SUBDIVIDE_2
  algorithm = osdbilinear
  iterations = 2
  group = WIRE_FITTING TIED_CURTAIN_CLOTH TIED_CURTAIN_BAND
          MAT_PAPER MAT_BOOK_COVER Ceiling Heater
```

墙体需要这些细分支撑扭曲。成功修复没有降低这两个级数，也没有把所有物体改成同一级别。历史截图曾出现约 1,275,536 个四边形，经 Divide 变成约 2,551,072 个三角面；这是当时版本的截图计数，不是成功版本所有帧的统一面数。

### 4. 先得到正确的静态展开

正确展开的目标：大平面能看出所属结构，墙上门窗开口保留，长条有连续性，每个材质集内部合理排在 0–1 并留边，避免意外重叠；曲面和小零件不强行变成长方形。

本次在低面数 `merge4` 源上完成以下工作，未对百万面动画逐帧运行 UV Layout：

1. 根据已有语义分组区分墙、地、顶、木头、金属、纸、书、布等。
2. 对墙、地、顶等缺少有效 UV 的硬表面，用一致的平面基准投影，将同平面且不互相覆盖的面组织成可读图块；保留墙体开口。
3. 对纸、书、窗帘等已有连续 UV 的部分尽量沿用；其他硬表面在整套静态预览中按平面整理。已做好的墙体展开继续保留。
4. 为图块按表面积调整密度并排布。静态脚本使用固定方向的确定性排布，按各材质集独立放入 0–1，按 2048 分辨率取约 4 像素单侧边距。
5. 检查数值有限、有效 UV 面积、范围，并检查写 UV 前后源点位置字节一致。小面积运算使用 float64，避免 float32 差分消去造成误判。
6. 用 Stash 保存实际几何和 UV，而非只保留 Shell 中的数组。分别查看墙体和其他分类，再保存预览 HIP。

最初静态排布算法曾离线检查整批 20,443 面的有效性与重叠；整套硬表面后续又整理过，不能把初版检查结果自动当成最终动画减面结果的证明。重新上传后的正确墙体 Stash 已实际解码、绘图检查，确认此前成功的大面布局仍在。

#### 15 个材质集与 UV 空间

| 最终分类 | 主要原分组／用途 |
| --- | --- |
| `ROOM_Walls` | `Wall__` |
| `ROOM_Floor` | `FLOOR` |
| `ROOM_Ceiling` | `Ceiling` 中的结构部分；灯具另分 |
| `ROOM_Windows` | `Window`、`BLINDS`，以及已核对的 18 个未分类窗台面 |
| `ROOM_Wood` | `MAT_WOOD`、`BLACKBOARD_WOOD`、`DOOR_WOOD` |
| `ROOM_Metal` | 暖气、门金属、框架、管线及夹件、图钉、线管配件、音箱金属等 |
| `ROOM_Fixtures` | `AC`、音箱主体与格栅 |
| `ROOM_Glass` | `DOOR_GLASS` |
| `ROOM_Blackboard` | 黑板背面、表面、粉笔与毛毡相关分组 |
| `ROOM_DisplayBoard` | `MAT_BOARD` |
| `ROOM_Paper` | `MAT_PAPER`、`MAT_POSTER` |
| `ROOM_Books` | `MAT_BOOK_COVER` |
| `ROOM_Tape` | `MAT_TAPE` |
| `ROOM_Curtain` | `TIED_CURTAIN_CLOTH`、`TIED_CURTAIN_BAND` |
| `ROOM_Lights` | `light`、`zhao`；原来与 Ceiling 组有包含关系，分类时作明确区分 |

每个材质集独立使用自己的 0–1 区域。因此整屋一起显示 UV 时，不同材质集会叠在同一画布；这不等于同一材质集内部发生错误重叠。**但本次曾出现单独显示墙体仍有跨图块大三角、棋盘格乱拉的情况，那是真正失败，不能用“只是叠加”解释。**

同样，三角形几何不等于逐三角形的碎 UV 岛；连通图块内部保留三角线正常。要看图块边界、连续性、开口以及模型上的棋盘格，而非只数内部线条。

### 5. 原始错误链与真正的覆盖点

```text
merge4
→ BOARD_WIRE_FACE_CHECK
→ BOARD_WIRE_FACE_FIX
→ SPEAKER_FACE_FIX
→ transform6
→ subdivide1 → DETAIL_SUBDIVIDE_2
→ normal1 → bend3 → merge14
→ divide1
→ uv_SP_FIX                 # 在动画后重新写 uv
→ divide2
→ polyreduce1 → clean4 → pack1 → rop_alembic1

divide1
→ timeshift1（frame = $F，并未冻结第 1 帧）
→ uvautoseam1 → uvflatten1 → uvlayout2
→ attribcopy1 的 input 1

uv_SP_FIX → attribcopy1 的 input 0
attribcopy1 → divide2 的 input 1（参考几何）
```

`divide2` 的第二输入不是可以随意删除的垃圾连线。SideFX Divide 支持参考几何输入用于凸化判断，使用其中的点位置；本文件 `timeshift1` 保留 `$F` 时间语义，旧切缝、展平、排布均只操作 `uv`。最终把这份位置参考直接接到 `timeshift1`，去除中间旧 UV 布局依赖，保留参考用途。

`attribcopy1` 在归档中的 `copydata` 为 off、`copyp` 为 on。不要仅凭其名称就假定它已经正确复制 UV，也不要对其他项目照搬本次参考输入改接；先核对该项目第二输入究竟是否改变位置或拓扑。

### 6. 最终成功接线：正确 UV 直接进入原动画

```text
merge4（原来的、可随时间更新的模型输入）
  ↓ input 0
ROOM_UV_ANIM_INPUT
  ↑ input 1 = ROOM_ALL_UV_20261124_234637_284042（正确 UV Stash）
  │ 只按对应面角写正式 vertex uv，不从 Stash 复制 P
  ↓
ROOM_UV_TAG_AS_TEXTURE
  │ setattribtypeinfo(0, "vertex", "uv", "texturecoord")
  ↓
BOARD_WIRE_FACE_CHECK → BOARD_WIRE_FACE_FIX → SPEAKER_FACE_FIX
  ↓
transform6 → subdivide1 → DETAIL_SUBDIVIDE_2 → normal1
  ↓
bend3（原节点、原关键帧、原控制器）→ merge14 → divide1
  ↓
divide2（input 0 = divide1；input 1 = 原 timeshift1）
  ↓
polyreduce1（原参数，seamattribs = * ^N）→ clean4
  ↓
ROOM_UV_ANIM_MATERIALS（按传下来的 15 类分配材质）
  ↓
ROOM_UV_ANIM_OUT（校验正式 UV、清理最终属性和分组；不重排、不缩放）
  ├─ ROOM_UV_ANIM_CHECK（仅棋盘格预览）
  └─ pack1 → rop_alembic1（原正式导出）
```

`ROOM_UV_ANIM_*` 名称是历史沿用；这些保留下来的节点现在只是 UV、材质与检查辅助，**并不代表仍使用复制的动画系统**。原 `bend3` 继续生效，后续修改原控制器和关键帧可以沿同一主链传下去。

成功安装时按原参数原始值及关键帧序列化结果作前后比较，核对变换、两级细分、法线、Bend、两个 Divide、PolyReduce、Clean 未被改写。UV 拷贝阶段另外核对源 `P` 字节不变。

**这里保留的是原节点、参数和动画控制，不是承诺最终网格逐点逐面字节一致。** PolyReduce 会考虑 UV 接缝；换成正确 UV 后，即使减面比例仍为 76.7%，也可能改变三角面合并选择。逐帧减面还可能产生拓扑变化，需要结合动画与最终导出检查。

#### 正确的 UV 复制单位是“面＋局部面角”

```python
target = g.findVertexAttrib("uv")
reference = r.findVertexAttrib("uv")
for dst_prim, ref_prim in zip(g.prims(), r.prims()):
    dst_vertices = dst_prim.vertices()
    ref_vertices = ref_prim.vertices()
    # 实际脚本在写入前检查每面点数、逐面点序和零件顺序。
    for dst_vertex, ref_vertex in zip(dst_vertices, ref_vertices):
        dst_vertex.setAttribValue(target, ref_vertex.attribValue(reference))
```

同样的点数、面数甚至逐面点序，并不能单独保证两个 geometry detail 的内部线性 vertex 存储顺序完全一致。之前直接跨 detail 拷贝整块 UV 字节数组只检查了拓扑，缺少这层保证。本次改为显式的面角对应，并以保存的 72,611 个参考面角测试了内部线性存储打乱时仍能正确复制。

这移除了一个不安全假设，**没有证明它是现场所有损坏的唯一原因**。成功版本同时修正了正式 UV 的接缝保护、旧展开覆盖以及旧布局依赖。

如果未来改变源模型、复制数量、面顺序、Boolean 或动态生成新面，应重新检查对应。拓扑或零件顺序不匹配时脚本停止；不使用最近点盲配，更不把静止 Stash 的位置替换进动画。

#### 分组与材质的保留顺序

在源 UV 拷贝节点中保留原始分组，并额外传递正确参考的 `ROOM_*` 分类。原分组仍被细分、翻面和动画使用，不能提前删除。只有全部几何处理完成后，才在最终输出清理旧分组，保留 15 个分类并统一 `material_name`、`shop_materialpath`。

旧 `unreal_material`、`material_id` 在最终输出中移除，避免残留旧材质标识与新分类打架；不删除原来的材质节点。几何分组、材质路径、Alembic Face Sets 与 SP Texture Sets 是相关但不同的机制，要分别确认。

#### 本次实际移除的旧处理

- 旧 UV 五个节点：`uv_SP_FIX`、`attribcopy1`、`uvautoseam1`、`uvflatten1`、`uvlayout2`。
- `uvquickshade2` 的查看输入改到 `divide1`，避免删除节点后留下旧依赖。
- 错误复制主链 `ROOM_ANIM_*`，以及复制的 `ROOM_UV_ANIM_PACK`、`ROOM_UV_ANIM_EXPORT_TEST`。
- 错误分支的临时墙体查看节点。
- 保留正确静态 Stash、原模型分支和原动画系统；不再携带 `uv_room_saved`，不再用整体缩放通过范围检查。

### 7. 本次排雷表：不要重复采用的做法

| 曾出现的问题／错误判断 | 现场证据与正确处理 |
| --- | --- |
| 因导出慢就降低墙体 Subdivide | 用户已经证明降低后形变不满足要求；保留原细分，先排查重复 UV 计算依赖 |
| 认为卡在 Divide 就一定是 Divide 独自耗时 | 第 39 帧的强制检查在请求 Divide 后无响应，但存在依赖计算和内存压力，不能据此孤立归因 |
| 忽略导出的 UV 旁支 | 后续崩溃画面明确显示 **第 23／40 帧，Cooking Op = uvlayout2**；这是旧 UVLayout 确实被请求的直接证据 |
| 在 Manual 下测到 0 秒／0 面就当真实性能 | 部分只读到了旧缓存或没有取得有效结果；需区分缓存状态与真正 cook |
| 对百万面逐帧重新 AutoSeam／Flatten／Layout | 产生重复工作和不稳定展开；静态低面数参考计算一次，存入 Stash，按对应传递 |
| 复制整套动画当作长期修复 | 复制参数和关键帧不等于保持与原节点的实时联动；最后直接使用原 `bend3` 主链 |
| 新 UV 使用 `uv_room_saved`，减面字段加入 `^uv_room_saved` | 实际失败文件中为 `* ^N ^uv_room_saved`，排除了新 UV 接缝保护。最终使用正式 `uv` 和原 `* ^N` 规则 |
| 只看 UV 数值范围正确就宣布成功 | 有序错误或跨图块连线仍可全部位于 0–1；还需看单材质图块、棋盘格和动画 |
| 全局缩小 UV 当作形状修复 | 失败版本将 UV 乘固定约 0.92357 以解决范围；这不能修复乱连、折叠或错误对应，后来单独墙体仍明显失败，最终撤销 |
| 把所有坏 UV 解释为不同材质叠加 | 整屋叠加有可能正常，但单独墙体仍乱就是实质错误，必须修传递链 |
| 只检查点数、面数，跨 detail 按整块字节复制 UV | 缺少面角／内部线性顺序一致性保证；最终明确按面及局部顶点写入 |
| 用静止几何替换动画输入 | Stash 只提供 UV，当前几何始终来自原 `merge4`；验证写 UV 前后 P 不变 |
| 提前删除所有旧分组 | 原细分过滤、翻面与控制器还用这些组；完成几何处理后再清理最终输出 |
| `Geometry.deletePrimAttrib` 等不存在的调用 | 实际报过 AttributeError；找到 `hou.Attrib` 后调用 `.destroy()`，分组用 `group.destroy()` |
| 给所有节点调用 `setDisplayFlag` | 创建导出副本时实际报 `RopNode` 无该方法；只对 `hou.SopNode` 设置 SOP 显示／渲染／模板旗标 |
| `needsToCook(time=...)` 在本机不兼容 | Houdini 21.0.440 实际报不接受关键字；采用 `.needsToCook()` 的无参数调用 |
| 误以为 `geometry()` 一定只读缓存 | `geometry()`、`geometryNoDep()` 会按需 cook；`infoTree(force_cook=False)` 也不保证跳过脏节点。缓存检查先核对 cookCount、needsToCook、errors |
| 长 Base64 脚本粘贴损坏 | 曾发生编码长度错误和 SyntaxError；改为可读 Python，使用整段 `exec`，不夹入 `>>>`／`...` 提示符 |
| 崩溃后依赖之前 Shell 的变量 | 临时恢复脚本只能用于当时会话；成功工程保存 Stash 和节点代码，重启不依赖旧内存 |
| 只看脚本结束／另存成功 | 安装完成不等于动画或导出通过；最终以代表帧、完整导出、SP 和 UE 结果共同确认 |

#### 44 个越界面角的实测记录

缓存检查在第 1 帧发现：

```text
直到 ROOM_ANIM_divide2：
  UV min ≈ (0.001953125, 0.001953125)
  UV max ≈ (0.997962475, 0.997410178)
  非有限值 0，越界 0

旧副本 ROOM_ANIM_polyreduce1：
  UV min ≈ (-0.002175637, -0.019204516)
  UV max ≈ (0.997962475, 1.016657948)
  非有限值 0，越界面角 44
```

这确定了该副本中**第一次范围异常**发生在 PolyReduce，并没有证明所有图块直到这一步都质量完好，也没有证明简单修正这 44 个数就能修好 UV。后续单独墙体视图证明确实还乱，统一缩放方案被否定。

### 8. 以后制作“正确 UV＋带动画模型”的顺序

1. **确定最终要用的源结构和数量。** 留出足够细分支撑所需变形；不要为了 UV 临时破坏造型、布尔或动画。
2. **在稳定的静止／未变形源上展开。** 按材质、结构、硬边规划图块，保持已有正确部分；按材质集检查密度、范围、边距与重叠。
3. **保存参考与对应关系。** Stash 或明确缓存几何；可变数量工程需要稳定的零件 ID 和局部面角 ID。只保存数组到 Shell 不算可恢复资产。
4. **只把 vertex UV 写回原动态源。** 明确面角对应并验证点位未改，不复制参考的静止 P；在会改变拓扑的后处理之前传入。
5. **让 UV 随后续处理自然插值。** 设置为 texturecoord，沿用原细分、翻面、法线和动画；删除或绕开后面会覆盖新 UV 的旧展开。
6. **检查 UV 与减面的关系。** 正式 UV 应参与既有接缝规则；不能一边让减面忽略新接缝，一边承诺新 UV 完全保留。若要严格锁定几何或动画拓扑，另行设计已验证的静止减面参考／缓存，不能盲接。
7. **最后整理输出材质与分组。** 保留制作阶段所需组到几何处理结束，最终再统一材质路径、名称与 Face Sets。
8. **同源导出静态与动画。** SP 使用最终链的参考帧模型，UE 使用同一最终链的动画；不能拿低面数原始 Stash 画完，再把不一致的最终 UV 动画放进 UE。
9. **验证代表帧，再完整导出。** 看正常状态、扭曲最大处和运动变化处；查看单材质 UV 与棋盘格，再做完整范围导出及 UE 检查。
10. **冻结可用基线。** 保存成功 HIP、对应单帧模型、动画 ABC、贴图和实际导出设置。后续改数量、源拓扑或 UV 时先另存，再重新核对同步关系。

### 9. 导出给 SP／UE：使用原正式节点

正式动画路径是 `/obj/classroom_generator/geo1/rop_alembic1`。它现在通过原 `pack1` 读取修复后的最终输出。`ROOM_UV_ANIM_CHECK` 是棋盘格预览，静态 Stash 是参考；两者都不作为另一个独立动画资产替代正式输出。

| 用途 | 设置示例（不是已回报的实际最终文件名） |
| --- | --- |
| SP 参考模型 | Alembic 单帧 `1 / 1 / 1`，例如 `E:/1120/ROOM_UV_SP_F1.abc` |
| UE 动画 | 实际起始帧／结束帧／步长 1，例如 `E:/1120/ROOM_UV_ANIM.abc` |

- 先保存修复后的 HIP。原归档 ROP 的范围曾为 `1–2`；导整段前必须主动填写真实范围，不能只改文件名。
- 保留 `Save Attributes`；vertex 属性模式 `*` 包括 `uv`、`N`。Face Sets 使用 **Save Non-Empty Groups as Face Sets**，核对导入后的 15 个材质分类。
- 采用 `Save to Disk` 执行；本次修复脚本不自动导出。后台另开进程可能额外占内存，并依赖已保存的 HIP，不作为初次验证的默认做法。
- Painter 支持 Alembic 输入；用最终第 1 帧文件创建项目，使用现有 UV，避免再次自动展开。贴图导出给 UE 的资产应来自这份最终 UV。
- UE 对该类变形动画使用 **Geometry Cache** 导入，核对材质槽、法线、采样时间和纹理附着。不要未经验证强行假设每帧拓扑恒定。
- Alembic 保存几何、UV、动画及面集等数据，不会把 Painter 的图层或 UE 材质图一并传过去；棋盘格也只是检查材质。

### 10. 为什么这次更快，以及哪些原因还不能断言

本次用户报告从此前约一小时且失败，改善为 40 帧、4 GB 多、十多分钟完成。与之对应的明确结构变化是：

- 正确 UV 在低面数源上计算并存好；动画计算时做明确的对应复制，不重新展开。
- 从正式导出依赖中移除了旧 UV Unwrap／AutoSeam／Flatten／Layout。
- 保留原动画主链，删除失败的复制动画与影子 UV 回写分支。
- 最终使用明确的 15 类材质／面集，避免残留旧分类混入输出。

这没有加入新的 Alembic 压缩设置，也没有为了提速降低已确认的细分级数。**尚未做控制变量 profiler／文件结构对比，不能精确分配各项加速比例，也不能把 4 GB 的体积变化全部归因于 UV、材质槽或某一种压缩。** 40 帧结果是该工程本次实测，不是对其他电脑／模型的耗时保证。

### 11. 留档：本次成功的专用改接脚本

<details>
<summary>展开完整代码：从本次 ROOM_UV_INSET 诊断工程迁移到原动画直接使用正确 UV</summary>

**仅适用于上述上传的诊断工程。已成功的 `ROOM_DIRECT_UV` 工程不要重复安装。** 脚本会检查预期节点与旧连接、先备份，另存新文件，并删除已经无效的旧展开和复制分支。不要当成任意 Houdini 工程都能运行的通用 UV 修复器。

在 Houdini Python Shell 中整段执行；源 Stash 和专用节点必须来自该工程。运行所需的 UV 复制、材质分配与末端校验代码保存在成功 HIP 的各节点中；本节完整安装器仅供一次性迁移留档，日常使用不必重跑。

```python
exec(r"""
import hou
import json
from datetime import datetime

net = hou.node('/obj/classroom_generator/geo1')
names = ['merge4', 'BOARD_WIRE_FACE_CHECK', 'subdivide1',
         'DETAIL_SUBDIVIDE_2', 'bend3', 'divide1', 'divide2',
         'timeshift1', 'polyreduce1', 'clean4', 'pack1', 'rop_alembic1',
         'ROOM_UV_ANIM_INPUT', 'ROOM_UV_TAG_AS_TEXTURE',
         'ROOM_UV_ANIM_MATERIALS', 'ROOM_UV_ANIM_OUT', 'ROOM_UV_ANIM_CHECK']
if net is None or any(net.node(s) is None for s in names):
    raise RuntimeError('请打开刚上传的 ROOM_UV_INSET 工程，节点不匹配，停止。')
if abs(hou.frame() - 1) > 0.001:
    raise RuntimeError('请先停在第 1 帧。')
nodes = {s: net.node(s) for s in names}
if nodes['BOARD_WIRE_FACE_CHECK'].input(0) != nodes['merge4']:
    raise RuntimeError('原链已经改变或已安装，不重复修改。')
bind = nodes['ROOM_UV_ANIM_INPUT']
ref = bind.input(1)
if ref is None or ref.name() != 'ROOM_ALL_UV_20261124_234637_284042':
    raise RuntimeError('正确 UV 的来源不匹配，停止。')
old_uv_names = ['uv_SP_FIX', 'attribcopy1', 'uvlayout2', 'uvflatten1', 'uvautoseam1']
if any(net.node(s) is None for s in old_uv_names):
    raise RuntimeError('旧 UV 分支与上传文件不同，停止。')
allowed_consumers = set(old_uv_names + ['divide2', 'uvquickshade2'])
for name in old_uv_names:
    if any(n.name() not in allowed_consumers for n in net.node(name).outputs()):
        raise RuntimeError('旧 UV 节点还有其他用途，停止：' + name)

hou.setUpdateMode(hou.updateMode.Manual)
rg = ref.geometry()
labels = sorted(g.name() for g in rg.primGroups() if g.name().startswith('ROOM_'))
if len(labels) != 15 or rg.findVertexAttrib('uv') is None:
    raise RuntimeError('正确 UV 的材质分组或顶点属性不匹配。')
paths = []
for label in labels:
    values = {p.attribValue('shop_materialpath') for p in rg.findPrimGroup(label).prims()}
    if len(values) != 1 or not next(iter(values)):
        raise RuntimeError('参考材质分配不一致：' + label)
    paths.append(next(iter(values)))

# Verify that the original deformation and geometry parameters are untouched.
watch_names = ['transform6', 'subdivide1', 'DETAIL_SUBDIVIDE_2', 'normal1',
               'bend3', 'divide1', 'divide2', 'polyreduce1', 'clean4']
watched = [p for s in watch_names for p in net.node(s).parms()]
before = [(p.rawValue(), tuple(k.asCode() for k in p.keyframes())) for p in watched]

bind_code = '''import hou
n = hou.pwd()
g = n.geometry()
g.clear()
g.merge(n.input(0).geometry())
r = n.input(1).geometry()
gp, rp = g.prims(), r.prims()
if len(gp) != len(rp) or g.intrinsicValue('pointcount') != r.intrinsicValue('pointcount'):
    raise hou.NodeError('源模型拓扑改变，停止复制 UV。')
for name in ('name', 'part'):
    if g.findPrimAttrib(name) is not None and r.findPrimAttrib(name) is not None:
        if g.primStringAttribValues(name) != r.primStringAttribValues(name):
            raise hou.NodeError('零件顺序改变：' + name)
before_p = g.pointFloatAttribValuesAsString('P')
point_uv = g.findPointAttrib('uv')
if point_uv is not None:
    point_uv.destroy()
target = g.findVertexAttrib('uv')
if target is None:
    target = g.addAttrib(hou.attribType.Vertex, 'uv', (0.0, 0.0, 0.0))
reference = r.findVertexAttrib('uv')
if reference is None or target.size() != reference.size():
    raise hou.NodeError('UV 属性格式不匹配。')
for dst, src in zip(gp, rp):
    dv, sv = dst.vertices(), src.vertices()
    if tuple(v.point().number() for v in dv) != tuple(v.point().number() for v in sv):
        raise hou.NodeError('面顶点顺序改变，停止：' + str(dst.number()))
    for a, b in zip(dv, sv):
        a.setAttribValue(target, b.attribValue(reference))
for source_group in r.primGroups():
    if source_group.name().startswith('ROOM_'):
        old_group = g.findPrimGroup(source_group.name())
        if old_group is not None:
            old_group.destroy()
        group = g.createPrimGroup(source_group.name())
        group.add([gp[p.number()] for p in source_group.prims()])
if g.pointFloatAttribValuesAsString('P') != before_p:
    raise hou.NodeError('位置校验失败。')
'''

material_code = 'int slot = -1;\n'
for j, label in enumerate(labels):
    material_code += 'if (inprimgroup(0, ' + json.dumps(label) + ', @primnum)) slot = ' + str(j) + ';\n'
material_code += 'if (slot < 0) { error("Missing UV material group"); return; }\n'
material_code += 'string labels[] = array(' + ','.join(json.dumps(s) for s in labels) + ');\n'
material_code += 'string paths[] = array(' + ','.join(json.dumps(s) for s in paths) + ');\n'
material_code += 's@material_name = labels[slot];\ns@shop_materialpath = paths[slot];\n'

final_code = '''import hou, numpy as np
n = hou.pwd()
g = n.geometry()
g.clear()
g.merge(n.input(0).geometry())
if g.findVertexAttrib('uv') is None:
    raise hou.NodeError('正式 UV 缺失，停止。')
uv = np.frombuffer(g.vertexFloatAttribValuesAsString('uv'), dtype=np.float32).reshape(-1, 3)
if not uv.size or not np.isfinite(uv).all():
    raise hou.NodeError('正式 UV 数据无效，停止。')
outside = int(np.sum(((uv[:, :2] < -1e-5) | (uv[:, :2] > 1.00001)).any(axis=1)))
print('最终 UV 检查，第', hou.frame(), '帧；越界角点：', outside)
for name in ('unreal_material', 'material_id'):
    a = g.findPrimAttrib(name)
    if a is not None:
        a.destroy()
for group in list(g.primGroups()):
    if group.name() not in LABELS:
        group.destroy()
'''.replace('LABELS', repr(labels))
compile(bind_code, 'bind_uv', 'exec')
compile(final_code, 'final_uv', 'exec')

stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup = 'E:/1120/ROOM_BEFORE_DIRECT_UV_' + stamp + '.hip'
target = 'E:/1120/ROOM_DIRECT_UV_' + stamp + '.hip'
hou.hipFile.save(file_name=backup)
print('备份已保存：' + backup)
ref.setDisplayFlag(True)

bind.parm('python').set(bind_code)
bind.setInput(0, nodes['merge4'])
info = nodes['ROOM_UV_TAG_AS_TEXTURE']
info.setInput(0, bind)
info.parm('class').set('detail')
info.parm('snippet').set('setattribtypeinfo(0, "vertex", "uv", "texturecoord");')
nodes['BOARD_WIRE_FACE_CHECK'].setInput(0, info)
nodes['divide2'].setInput(0, nodes['divide1'])
nodes['divide2'].setInput(1, nodes['timeshift1'])
old_checker = net.node('uvquickshade2')
if old_checker is not None:
    old_checker.setInput(0, nodes['divide1'])

materials = nodes['ROOM_UV_ANIM_MATERIALS']
materials.setInput(0, nodes['clean4'])
materials.parm('class').set('primitive')
materials.parm('snippet').set(material_code)
out = nodes['ROOM_UV_ANIM_OUT']
out.setInput(0, materials)
out.parm('python').set(final_code)
nodes['pack1'].setInput(0, out)
nodes['ROOM_UV_ANIM_CHECK'].setInput(0, out)

if [(p.rawValue(), tuple(k.asCode() for k in p.keyframes())) for p in watched] != before:
    raise RuntimeError('原参数校验不一致，请恢复备份：' + backup)

# Save the working connections before removing obsolete nodes.
hou.hipFile.save(file_name=target)
obsolete = old_uv_names + [n.name() for n in net.children() if n.name().startswith('ROOM_ANIM_')]
obsolete += ['ROOM_UV_ANIM_PACK', 'ROOM_UV_ANIM_EXPORT_TEST',
             'ROOM_FINAL_WALLS_CHECK', 'ROOM_FINAL_WALLS_VIEW']
for name in obsolete:
    node = net.node(name)
    if node is not None:
        node.destroy()

bind.setComment('按对应面角复制正确 UV；原位置和动画输入保持。')
out.setComment('原动画链的正式 UV 输出；没有重新展开或缩放。')
check = nodes['ROOM_UV_ANIM_CHECK']
check.setRenderFlag(False)
check.setDisplayFlag(True)
check.setSelected(True, clear_all_selected=True)
hou.hipFile.save(file_name=target)
print('已另存：' + target)
print('原细分、变形、减面参数及关键帧校验一致。')
print('原动画仍使用原 bend3；正式导出仍是原 rop_alembic1。')
print('旧 UV 展开和失败副本已删除；没有执行导出。')
print('现在只更新第 1 帧的模型和 UV；未执行导出。')
hou.setUpdateMode(hou.updateMode.AutoUpdate)

""")
```

</details>

### 12. 后续接手时的优先级

1. 用户说“教室墙体／本体”时，优先打开并核对 `ROOM_DIRECT_UV_20261125_004415_787159.hip`，读取原主链和本节；不要重新运行复制动画、影子 UV、INSET 缩放或旧全场景展开脚本。
2. 保留正确 Stash，不把“旧参考”一律当垃圾删除；当前成功工程重启后可直接继续，不需要旧 Shell 数据。
3. 材质、灯光和镜头工作在这个已跑通的 UV／动画基线上进行。桌椅 `/obj/other` 的验收状态按下一节单独判断，不能因本体 40 帧成功就改写成桌椅所有问题均已完成。
4. 需要新检查时，先读实际缓存和依赖，不再默认强制 cook 第 39 帧全链；只在有新失败或明确验证需求时扩大测试。

参考：[SideFX Divide 的参考几何输入](https://www.sidefx.com/docs/houdini/nodes/sop/divide.html)、[PolyReduce 的顶点属性接缝](https://www.sidefx.com/docs/houdini/nodes/sop/polyreduce.html)、[VEX texturecoord 类型](https://www.sidefx.com/docs/houdini/vex/functions/setattribtypeinfo.html)、[HOM Vertex](https://www.sidefx.com/docs/houdini/hom/hou/Vertex.html)、[Painter 导入格式](https://experienceleague.adobe.com/en/docs/substance-3d/general-knowledge/ecosystem/import-and-export-formats)。

---


## 2026-11-24：改变椅子数量、替换书本后的 UV 修复

本节记录 `/obj/other` 桌椅的 11 月 24 日修复；教室本体的最新成功见上节。后文保留早期流程与历史问题，不应把旧的“待运行”记录误认为本次桌椅补丁没有执行。

### 已保存版本与验收证据

- 原工程：`E:/1120/1124.hip`，未被本次成功脚本覆盖。
- 操作前备份：`E:/1120/1124_BEFORE_UV_20261124_151657_073664.hip`。
- 成功另存版本：`E:/1120/1124_UV_CHECK_20261124_151657_073664.hip`。
- 局部诊断数据：`E:/1120/1124_UV_remaining_two.json`。
- 用户截图显示脚本输出 `UV_APPLIED`、`BOOK_UV_CONNECTED`，并成功保存新版本；用户确认本次结果可用。
- 截图包含第 1 帧静止排列和第 48 帧异化运动时的棋盘格预览。脚本另外核对了第 1、40 帧源桌椅的逐面顶点数及逐面点序一致。
- 以上属于脚本检查、用户反馈与代表帧画面证据；**不是全部动画帧、所有零件近景、SP 重新绘画和 UE 完整 Alembic 导入均已验收。**

### 成因：旧的全场景编号不能直接用于新数量

上传的五个 `1124.7z.001`～`.005` 已合并解压得到 `1124.hip`。离线解析 HIP 的连接、参数及锁定几何，再由用户在本机 Houdini 执行补丁；分析环境没有启动 Houdini。

| 数据 | 点 | 面 | 面角／顶点 |
| --- | ---: | ---: | ---: |
| 当前 `merge4` 桌椅 | 800,880 | 752,180 | 3,034,720 |
| 旧 `IRON_TINY_AREA_FIXED_UV` | 679,710 | 632,040 | 2,554,240 |

`DESK_FINAL_UV_ON_ANIMATED_DESKS` 原来将当前 `merge4` 与旧锁定参考按 vertex 编号对应；数量及排列变化后，这个全场景对应已失效。仅重建数量一致的普通 UV Layout 会丢掉此前木头、铁件的展开与修复结果，不能作为保留现有工作的修复方法。

### 成功方法：按独立连通零件复用已有 UV

1. 在第 1 帧取得当前源桌椅几何，保留点、面、材质和分组；只准备替换 vertex `uv`。
2. 用共享点连接关系分离零件。旧锁定参考中识别出 **5,179 个连通零件**。
3. 根据零件点数、面数、逐面角数和局部点连接序列构造拓扑签名。先比较去平移后的坐标，再以最小二乘仿射拟合验证旋转、缩放等对应；检查最大残差和点集秩，避免接受退化映射。
4. 匹配后按明确的局部面角对应复制旧 UV；**不运行整班 UV AutoSeam／Flatten／Layout**。因此保留原有桌面及铁件的 UV 结果，重复椅子零件可复用旧零件 UV。
5. 对两个完整拓扑不同的局部零件，使用下述离线验证的部分面对应，不猜测最近面、不盲目放宽误差。
6. 验证所有面角有 UV、数值有限；核对代表帧源拓扑；验证写 UV 前后源点位置字节一致。
7. 用 Stash 节点 `UV_VERIFIED_REFERENCE_1124` 保存当前数量的参考，接到 `DESK_FINAL_UV_ON_ANIMATED_DESKS` 的 input 1。input 0 保持原动画源，原 Divide／Edit／PolyReduce 链与动画参数保留。
8. 先保存操作前备份，再接入补丁，最后另存 `1124_UV_CHECK_时间戳.hip`。异常时恢复修改的输入连接并移除新建参考。

这是为当前版本**重建一次正确对应**，不是已经实现任意改数量、任意换拓扑都自动稳定的系统。Stash 是当前数量的静止快照；以后继续改变源模型、复制数量或顺序，仍需重新检查和构建对应。相同零件复用旧 UV 可能共享 UV 区域；若要逐把椅子独立绘画，需要另行规划实例差异或图集。

源几何点位保护不等于已经证明所有下游结果逐点不变：UV 接缝可能影响既有 PolyReduce 的重新计算，最终减面形状仍需看预览及导出验证。

### 两个特殊零件：完整拓扑不同，但剩余面仍有对应

早期只允许平移的版本剩 86 个零件未匹配；增加仿射对应后剩 2 个。前几次脚本因整体校验不通过而在接线前停止，**没有真正应用桌椅或书本的修改**。不能把这些停止提示解释成修复完成。

用户导出两个局部零件的点、面、原始面号和面角号为 JSON 后，离线完成了具体对应：

| 零件 | 当前点数 | 当前四边形数 | 当前面角数 | 旧参考面角范围（零起点、右端不含） | 最大坐标拟合误差 |
| --- | ---: | ---: | ---: | --- | ---: |
| 局部零件 A | 124 | 100 | 400 | `[640, 1040)` | 约 `1.03e-6` |
| 局部零件 B | 252 | 240 | 960 | `[55856, 56816)` | 约 `1.12e-6` |

A 使用边邻接与有向面角关系确定旧零件的部分面，再验证坐标拟合；B 与旧 252 点、250 面零件的点对应成立，保留了其中 240 面。修复只恢复保留面角的 UV，**没有补回缺少的面，也没有改变当前模型**。

用 float64 计算这两个零件共 340 个面的 UV 面积，均有效、非零。直接用 float32 做小 UV 多边形的面积差可能出现消去误差，不应误判为 UV 坍缩。

硬编码面角范围仅用于已验证的 `1124.hip` 参考；脚本必须核对原参考 vertex UV 数据的 SHA-256：

```text
d1bf7481a83f134fe66f17e0bf25197b48e66a027cc7cb08509930191cfbcfd3
```

同时核对 JSON 指定面角的当前位置与顺序。**其他版本不可照搬这两个范围。** 旧参考自身回映射测试也已通过：5,179 个零件映射回自身后，UV 数组完全一致；该测试只验证回映射，不替代当前场景的运行和画面检查。

### 书本：保留源 UV，绕过错误的旧全场景复制

实际旧链为：

```text
merge1（当前书本／纸笔＋被标记的原桌椅）
→ attribcopy1（从 DESK_FINAL_ORIGINAL_UV_LOCKED 按旧编号覆盖 UV）
→ DESK_FINAL_KEEP_ORIGINAL_BOOKS_AND_PENS（删除标记桌椅）
```

替换书本模型后，先覆盖旧 UV、后分离书本，会把新书本自身正确的 UV 破坏。成功补丁把保留节点的 input 0 直接接到 `merge1`，继续删除 `desk_uv_replace_exact` 桌椅组，从而保留当前源书本／纸笔 UV，再与修复桌椅合并到 `DESK_FINAL_REPLACE_DESKS_ONLY`。

补丁检查源分支具有 vertex UV 且过滤组存在；没有改书本模型或其动画。存在 UV 属性本身不代表所有面的质量通过，最终仍结合用户预览确认。不要为了修书本而重新展开桌子。

### 可恢复脚本要求

- 用户不能直接下载脚本；交付可复制的 Houdini Python Shell 代码，或 PowerShell 写本地脚本后再执行。
- **最终脚本必须独立运行**，从 HIP 重新读取数据，不能依赖上一段 Shell 留下的 `current`、`buckets`、`assigned` 等变量。崩溃或重启会清除这些变量。
- 本次最终版本的 Stash 已随新 HIP 保存；重启不依赖旧 Shell 内存。
- 保留检查 JSON，它是再次运行这个特定补丁的外部输入。不要误称 HIP 已包含全部外部资源。
- 只备份／另存请求的 HIP，不复制整个资源目录。先检查现有工程、参考哈希和连接，再修改。
- 不得为了修 UV 改数量、布局、动画、Boolean 或删除旧回退参考；避免再次对整班做全新展开。

### 教室本体导出耗时：11 月 24 日历史诊断，已由新成功记录更新

这是 `/obj/classroom_generator/geo1` 的独立问题。早期用户报告约一小时导出并在第 39 帧附近失败，当时尚不能确定具体耗时节点，也不能认定点击屏幕导致失败。

早期核对到 `uv_SP_FIX` 在 `bend3` 后、`polyreduce1` 保留 76.7%、`timeshift1` 使用 `$F` 而非冻结帧，导出四类属性模式均为 `*`，全部非空组输出为 Face Sets。上传的早期 ROP 范围为 `1–2`、路径为 `E:/1120/space4.abc`，不等于用户失败长导出的完整设置。

随后尝试强制计算第 39 帧：请求 Divide 后无响应且内存上升，用户结束进程；没有得到可信的完整单帧性能分解。之后另一次导出在第 23／40 帧崩溃，界面明确显示正在计算 `uvlayout2`。因此不能继续把“卡在 Divide”当成唯一根因，也不再把重跑第 39 帧全链作为默认下一步。

本次重新读取的版本含两个按分组分工的细分节点（3 级与 2 级），并非无条件对所有教室物体做 3 级；实际过滤规则见[11 月 25 日成功记录](#room-uv-animation-20261125)。最终保留原细分和动画，去除旧 UV 展开依赖，以正确 UV 直接进入原主链，用户已完成 **40 帧、4 GB 多、十多分钟** 的导出并展示 SP／UE 结果。旧“尚未提速、尚无完整导出”的状态只描述当时，现已被本次结果更新。

---

## Procedural Workflow

### 1. 静止参考 UV → 动画几何

已经采用的流程：

1. 从桌椅合并几何取得第 1 帧静止参考。
2. 建立切缝，展开并排列 vertex UV。
3. 锁定参考结果。
4. 将 vertex `uv` 复制到具有相同拓扑和顶点对应关系的动画几何。
5. 让 UV 随既有位置动画及后续几何处理传递，不在每个动画帧重新展开。

桌椅部分：用户已观察到木头和部分铁件可在 SP 绘画，多帧运动时纹理基本附着；书本原本已有正确 UV，应保护。**该桌椅补丁的整段导出仍按其独立证据验收。** 教室本体则已于 11 月 25 日完成 40 帧导出，见上方成功记录。

#### 重要边界：这是按顺序复制，不是稳定 ID 匹配

此方法依赖点数、面数、顶点数、逐面点序和顶点对应关系一致。

- 不是只修某一个动画帧。
- 也不是已经实现“每把桌椅按独立 ID 自动匹配 UV”。
- 数量相同也不能证明顺序相同。
- 改变复制数量、顺序、源模型结构或 Boolean 拓扑后，旧参考可能失效。
- 从 20 椅改为 25 椅，必须重建对应静止 UV 参考，并检查依赖拓扑的 Edit 和减面参考。2026-11-24 已通过按零件复用旧 UV 重建当前参考，详见最新记录；不是重新展开整班。
- 若未来需要可变数量，应在复制、变形前建立稳定的 `piece_id` 和局部顶点 ID，再进行明确映射。

### 2. 统一纹理密度

在锁定的静止参考后添加 UV Layout，只处理指定材质组，开启 **Scale Islands to Match Their Surface Areas**（当前版本内部参数 `correctareas`），计算后再次锁定，再接回动画 UV 参考输入。

| 组 | 当前用途 |
| --- | --- |
| `MAT_WOOD` | 木头 |
| `MAT_IRON` | 铁件 |
| `MAT_DOWN` | 脚垫／下部相关分组，实际材质需核对 |

木头与铁件密度调整均有用户运行完成记录；木头棋盘格和 SP 材质表现明显改善。

**限制：**统一岛平均密度不会自动修复岛内部拉伸、坍缩或错误接缝，也不会自动对齐木纹方向。小倒角、螺丝、挂钩产生小岛是正常现象，不等于多生成模型。

参考：[SideFX UV Layout](https://www.sidefx.com/docs/houdini/nodes/sop/uvlayout.html)。

### 3. 在进入减面前携带正确 UV

以下是 `/obj/other` 桌椅历史方案：先前观察到 `merge4`、`divide2`、`edit4` 的数量在检查帧间相同，而原 `polyreduce3` 输出数量变化。桌椅修复分支在减面前传递 UV，并为克隆减面节点提供静止参考。教室本体最终使用原动画主链，不要将这个桌椅方案机械套入教室。

数量变化本身不必然证明 UV 错误，但不能在未确认对应关系时，把静止减面输出的 UV 按索引强行复制给另一个动画减面输出。

参考：[SideFX PolyReduce](https://www.sidefx.com/docs/houdini/nodes/sop/polyreduce.html)。

## Node Breakdown

下表为 `/obj/other` 桌椅已分析版本的关键名称；教室本体另见上方成功主链。**新接手时必须读取实际连接，不按项目文件名猜版本。**

| 节点／路径 | 作用 |
| --- | --- |
| `/obj/other` | 主对象网络 |
| `merge4` | 源桌椅合并 |
| `MOVEABLE` | 桌子可动结构，内部包含 `METAL_CUBBY`、`LEG_UP`、`WOOD`、孔洞、螺丝及 Boolean |
| `STABLE`、`SETTEL`、`MOVEABLE1`、`subnet1` | 其他固定／可动源结构，具体职责以连接为准 |
| `DESK_FINAL_REST_1` | 静止参考 |
| `DESK_FINAL_SEAMS` | 切缝 |
| `DESK_FINAL_FLATTEN` | 展开 |
| `DESK_FINAL_UV_LOCKED` | 锁定桌椅 UV |
| `WOOD_DENSITY_FIXED_UV` | 木头密度调整后的参考 |
| `IRON_DENSITY_FIXED_UV` | 铁件密度调整后的参考 |
| `IRON_SIDES_FIXED_UV` | 部分后续项目中的侧面修复参考；并未证明所有外壳都修好 |
| `DESK_FINAL_UV_ON_ANIMATED_DESKS` | vertex UV 传递；input 0 为动画几何，input 1 为当前锁定参考 |
| `DESK_FINAL_divide2`、`DESK_FINAL_edit4`、`DESK_FINAL_polyreduce3` | 修复桌椅的后续处理 |
| `DESK_FINAL_REDUCE_REST` | 克隆减面的静止参考 |
| `DESK_FINAL_MARK_OLD_DESKS` | 标记原桌椅分支，使用 `desk_uv_replace_exact` |
| `DESK_FINAL_KEEP_ORIGINAL_BOOKS_AND_PENS` | 保留原流程非桌椅几何 |
| `DESK_FINAL_REPLACE_DESKS_ONLY` | 合并保留内容与修复桌椅 |
| `uvquickshade1` | 通常为最终预览 |
| `IRON_SIDES_REFERENCE_PREVIEW` | 临时静止参考预览，不是动画导出节点 |

用户原有 `edit4` 包含修形／移除多余椅子的操作。改变复制数量后这些选择也可能失效，不要盲目删除或继续沿用。

历史导出链包含：

```text
最终修复结果
→ divide1
→ polyreduce1
→ clean1
→ pack3
→ rop_alembic1
```

导出前核对实际连接。无实际 UV 的上游 `uvquickshade3` 曾显示自动投影，不能据此证明最终 UV 稳定。

## Troubleshooting

### 金属外壳／上段杆：UV 没消失，而是过小

表现：桌斗内侧、上下表面及部分横杆有格子，左右外侧板和部分上段杆却没有正常格子，SP 中难以绘画。

#### 文件与证据来源

四个 `UV.7z` 分卷已成功合并、解压。归档中实际文件为：

```text
final_R_IRON_UNIFORM_20261120_004535.hip
```

这是统一铁件密度版本，**比后来的 `IRON_SIDES_FIXED` 更早**。

执行环境没有启动 Houdini，而是解析 HIP 中保存的锁定几何数据。静止桌椅参考包含：

- 679,710 点；
- 632,040 面；
- 2,554,240 顶点。

示例面号仅适用于该归档对应拓扑：

| 面号 | 实际面积 | UV 面积 | UV 面积／实际面积 |
| --- | ---: | ---: | ---: |
| 115036 | 约 0.698602 | 约 3.76048e-10 | 约 5.38286e-10 |
| 115039 | 约 0.698602 | 约 3.73846e-10 | 约 5.35134e-10 |
| 115054 | 约 0.358679 | 约 4.75220e-12 | 约 1.32492e-11 |

正常大块铁件的面积比例约为 `0.00114`。示例侧板的比例比它小约两百万倍。

**旧检查只判断 UV 面积小于 `1e-12`，漏过了这些实际面积很大、UV 仍有微小非零面积的面。**

新补丁的判定原则为：

```text
实际面积有效，并且：
UV 绝对面积极小，或 UV 面积／实际面积极小
→ 在静止参考中重新投影异常铁面
→ 重排铁件 UV
→ 锁定并沿用原动画传递
```

当前补丁相对密度阈值是 `1e-7`，这是本项目的修复参数，不是通用标准。微小倒角、近退化面和浮点误差需要考虑。

#### 验证状态

- 归档数据的数值检查证明新条件能命中上述侧板与杆件。
- 旧 `IRON SIDES DONE` 只证明旧脚本完成，不代表外壳全部修好。
- **最新 tiny UV 补丁尚未收到用户运行成功及完整动画导出通过的确认。**
- 不得将当前金属问题写成“已彻底修复”。
- Boolean 可能影响拓扑和属性，但目前不能证明它是唯一成因；不要直接删除外盒或布尔节点。

### 木头：密度与朝向是两件事

密度已有改善，部分主要桌面 UV 岛仍斜放。

UV 岛旋转不等于模型变歪，也不必然意味着拉伸，但影响二维绘画与木纹方向统一。后续应按桌面局部方向对齐主要岛，再在保持方向的情况下排列；不要强行把全部倒角碎岛变成正方形。

### DefaultMaterial 与材质归属

材质组、`shop_materialpath`、导出材质槽、Painter Texture Set 是不同概念，必须分别检查。

归档中确实有部分 `/shop` 材质路径。不能把所有 DefaultMaterial 面一律改为铁件，也不能仅根据名称猜测零件。可在 SP 临时填充醒目纯色以定位，完成后移除测试层。

任何 UV 更新都应同步 Painter 输入网格及 UE 对应静态／动画资产。已有笔触可能需要重投射；不要承诺自动保留。不能只在 Painter 修改 UV，继续使用 UE 旧 UV 动画。

### 脚本与操作经验

- 交付方式：**直接提供可复制的 Houdini Python Shell 代码，或 PowerShell 写入本地脚本后执行**。用户无法直接下载脚本文件；脚本必须可独立恢复运行。
- PowerShell 提示符是 `PS C:\...>`；Houdini Python Shell 提示符是 `>>>`。每段明确运行位置。
- 文件未生成时不要反复执行 `open`；先确认生成步骤。
- PowerShell 多条命令放入整体 `& { ... }`，并设置 `$ErrorActionPreference='Stop'`，避免报错后继续写出不完整脚本。
- 补丁必须验证匹配次数；避免脆弱的无检查文本替换。
- 子网络输入连接的 `inputNode()` 可能为 `None`。
- 子节点包含 `RopNode`，不可对所有节点调用 SOP 专属方法。
- Ramp 参数不能直接 JSON 序列化；报告需显式转换，或使用 `default=str`。
- 删除 `hou.Node` 前先从列表移除；已删除节点参与相等比较可能触发 `ObjectWasDeleted`。
- 先备份、另存短文件名；检查失败恢复原连接。
- “脚本结束”不等于“最终画面与全段动画通过”。

## Unreal Engine Integration

### 桌椅与静态／动画切换的后续验收顺序

教室本体已完成本次完整导出和 SP／UE 画面确认；下列待办主要针对桌椅和整套镜头切换，不回退本体已确认的成功状态。

1. **金属修复**：近看桌斗左右外侧、内侧、上下表面、上段杆、横杆、挂钩；检查覆盖、密度和拉伸，不只看 DONE。
2. **静态版**：确认 25 桌＋25 椅，使用自己的有效 UV；一帧导入 SP，检查材质槽、绘画覆盖、UV 面积和木纹方向。
3. **动画版**：保留镜头与运动，先测代表帧，再导出完整 40 帧到 UE。
4. **UE 检查**：UV 滑动、拓扑跳变、穿插、材质丢失、静态／动画切换穿帮。
5. **切换逻辑**：资产与镜头通过后再连接蓝图触发。

40 帧的起止范围、帧率和端点包含方式，以实际 Sequencer 安排为准。SP 单帧通过不代表整段动画通过。

### 性能现状

**最新教室本体实测：40 帧、4 GB 多、十多分钟完成；没有改成另一套动画，也没有降低原细分。** 结构变化与归因边界见上方成功记录。

以下保留此前桌椅／旧链的历史记录：用户曾报告每帧导出耗时约翻倍，当时尚未 profiling 确认。

可能存在旧桌椅链与克隆修复链重复计算，不可未经测量断言。归档含四份大型锁定几何快照，是 HIP 较大的原因之一；不要为了省空间删除唯一可回退参考。

锁定 UV 应避免每帧重新展开。先测 cook 与写盘耗时，再决定缓存策略。缓存首次生成加导出不一定更快，主要有利于后续重复使用。

## Results & Next Steps

### 状态总表

| 项目 | 当前状态 |
| --- | --- |
| 最新桌椅＋教室组合 | 2026-11-26 的 `E:/1126/1126.hip`；用户打开正确文件并确认第 20 帧组合形态接近理想效果，详见最新记录 |
| 本次完整资产合并 | `/obj/other` 全部 1,966 条记录来自 tableright；其他 1,715 条含结束标记的记录保留基底；逐条及全文件校验通过 |
| 本次组合版本的整段／导出 | 尚无新增完整片段、全 UV、SP／UE 或 ABC 导出验收；历史本体导出成功不替代本次验收 |
| Houdini → SP → UE 链路、HDRI | 用户确认已跑通／准备 |
| 教室本体正确 UV | 2026-11-25 直接写入原动态源；原细分、Bend、几何处理参数与关键帧保持，成功基线 ROOM_DIRECT_UV |
| 教室本体材质分类 | 最终 15 个 ROOM_* 分类；用户 SP 列表与 UE 带材质画面确认 |
| 教室本体完整 40 帧 | 用户确认 4 GB 多／十多分钟导出完成，已展示 UE 弯曲状态；未逐帧逐面自动验收 |
| 书本源 UV | 2026-11-24 已绕过旧全场景 UV 覆盖；用户确认预览可用，SP／UE 新版本仍需验证 |
| 改数量后的桌椅 UV | 2026-11-24 按零件复用旧 UV、补齐两个部分面对应并另存成功；第 1／48 帧截图与用户反馈确认当前预览可用 |
| 桌椅静止参考 UV 传递动画 | 已有多帧附着的用户观察；桌椅专属全段状态与本体独立 |
| 木头纹理密度 | 已运行并明显改善 |
| 部分铁件与横杆 | 已改善 |
| 桌斗外侧板、部分上段杆 | 小 UV 成因已由归档数据确认；最新补丁待运行与画面验收 |
| 木头主要 UV 岛朝向 | 待处理 |
| 25 桌＋25 椅静态版 | 制作决策已确定，最终导出与材质待验收 |
| 桌椅动画版完整 40 帧 | 专属导出及近景问题仍需独立确认；不能以本体成功代替 |
| 蓝图切换 | 后续工作 |

### 后续 Codex 接手顺序

1. 先读 [1126 合并成功记录](#baseline-1126-merged-20261126)，以 `E:/1126/1126.hip` 为最新用户认可的组合基线，核对完整打开路径及用户这次授权的修改范围。
2. 查阅 `records/houdini/2026-11-26-1126-merge/` 中的来源清单、逐节点快照与已运行脚本。保持 `tableright.hip`、`wallright.hip` 两份正确来源不变；不要误用 `_merge_rollback/1126.hip`。
3. 按当前任务继续局部完善或材质、灯光、镜头工作。旧 1124 桌椅和 11 月 25 日教室记录用于理解技术，不自动替代当前基线或证明本次全段导出已经通过。
4. 只有用户实际指出新的缺陷才针对该范围诊断；不要重新展开整班、重建动画、修改已认可的另一部分，或重复执行旧失败补丁。

### 墙体沿用的原则

此原则已用于上方本次教室成功修复：在选定的低面数源上建立 UV，在原细分与变形前按对应写回正式 UV，动画帧间不重复展开。未来改源拓扑时重新检查对应。

若墙体逐帧 Boolean、切割或生成新面，应先设计稳定分块、预切模型或可验证映射；**不能直接把冻结帧 UV 按顶点顺序复制到变化拓扑。**



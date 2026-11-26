# Substance Painter AI Codec

## 2026-11-26 · 旧石灰灰泥与 Painter Python 工作流

目标是给教室墙面、天花板和梁制作写实旧灰泥。参考特征是浅灰米白的残留罩面、偏暖灰的露底、沿刮刀方向拉长的抹痕，以及近看才明显的细砂孔。案例在 Windows 的 Substance 3D Painter 12.2.0 中操作，测试纹理集在界面上显示为 `ROOM_Ceili...`，分辨率为 2048 × 2048。

## 从参考图到填充层

1. 给 AI 两张图，一张材质参考，一张包含纹理集、图层和视口的 Painter 截图。说明应用面、期望尺度和写实目标。
2. 第一版用外部 Python 生成可平铺的 Base Color、Roughness 和 16 位 Height。已在外部环境生成并检查 4096 × 4096 PNG 的位深与平铺边缘。这个检查只覆盖贴图生成。
3. 为了省掉终端、安装依赖和手动搬文件，改成可整段粘贴到 Painter 的 Python 控制台的标准库版本。实际使用 2048。该版本是独立改写，外部版本的 4K 检查结果不能直接套用。
4. 选中目标纹理集，检查 Base Color、Roughness、Height 通道。脚本将 PNG 作为 Texture 导入当前项目，在图层栈顶部创建 `Weathered Lime Plaster` 并绑定通道，使用三平面投射。若有 Metallic 通道，将灰泥设为非金属。
5. 先在 Base Color 视图看露底比例和投射尺度，再用材质视图的侧光检查真实起伏。检查当前纹理集和图层名后再继续，避免重复创建填充层。

## 故障记录

| 表现 | 原因和处理 |
| --- | --- |
| `This method can't be called from a ScopedModification`，堆栈指向 `set_selected_nodes` | 脚本把选层放进了批量修改块。图层和通道设置已经执行到最后，现场确认材质层存在。下次将 `ls.set_selected_nodes([layer])` 移到 `with ls.ScopedModification(...)` 块外。已有图层时直接手动选中或在块外选中。 |
| 视口有斑驳，但保存和另存为都失败 | 日志先报 `ResourceImage` 无法从 `.../Temp/painter_lime_plaster_.../LimePlaster_Roughness.png` 加载图像，之后报无法对空曲面进行序列化。后续也见到 Height 的读取错误。生成脚本退出 `TemporaryDirectory` 时删除了源图，Painter 保存时仍需要读取它们。 |
| 回填脚本找不到 `make_lime_plaster` | 当前控制台命名空间里没有旧函数。恢复脚本应当自包含，包含所有导入、函数和入口，以便在不同的控制台执行上下文里使用。 |
| 回填脚本报 `NameError: name 'struct' is not defined` | 在控制台执行多行 `exec` 时，嵌套函数没有从预期作用域获取顶层导入。成功版本把 `struct`、`zlib`、`Path` 放到入口函数内，并用 `exec(code, {})` 给代码块提供一致的全局命名空间。 |

## 保存失败时的恢复顺序

1. 在关闭提示里点「取消」，保留当前工程。打开 Log，看本次保存失败前第一条 `ResourceImage` 报错，记下文件名和完整路径。
2. 优先把原 PNG 恢复到日志显示的**原路径**。生成记录可用时，沿用原生成器、分辨率、seed 和 wear。此案例控制台版使用 2048、seed 41、wear 0.48。外部版与控制台版算法有差异。
3. 原图无法立即恢复时，在原目录只为缺失文件写入有效 PNG。案例使用 2048² 的 RGB 8 位 Base Color 占位、灰度 8 位 Roughness 占位、灰度 16 位 Height 占位。已有文件保留。Roughness 用约 0.82，Height 用中灰。保留现有图层和资源绑定，随后另存为新的 `.spp`。
4. **已验证结果**是补回占位 PNG 后，用户确认项目可以保存。占位通道的灰泥细节仍需恢复。后续在固定目录生成正式 PNG，重新绑定现有填充层，再保存并重开副本检查各通道和日志。

以后将生成文件放到固定的可写项目资源目录。保留源文件，并用另存后的副本验证关闭、重开和重新保存。看到视口有图案只是第一步，三通道可读、工程能保存和重开才完成验证。

## 材质为什么会显得像橡皮泥

早期版本用整个露底遮罩驱动 Height，白梁在光下显得圆鼓。参考中的大部分斑驳应由 Base Color 表达，浅层露底可带少量粗糙度差异，高度主要留给薄剥落边、细刮痕和砂孔。

在 Painter 中可先把 `Weathered Lime Plaster` 的 **Height 通道不透明度**降到 0%，看同一根白梁，再从约 10% 逐步加回。若鼓包仍在，逐个检查下方 V07 图层的 Height 和 Normal。若轮廓已经平硬但颜色还像迷彩，调整灰白过渡、斑块形状和刮痕方向。Designer 可用于分别控制宏观露底、刮刀痕和微观孔隙，再把对齐的 PBR 通道交给 Painter 投射。这个分工是下一轮方案，本次没有在 Designer 实作。

## 交给下一个 AI 的协作约定

- 默认交付能直接粘贴到 SP Python 控制台的自包含代码。导入放进函数，明确入口与参数，避免依赖之前运行过的脚本、外部终端或第三方包。
- 操作者在 Windows Painter 中选择纹理集、执行脚本、保存工程并提供日志。AI 根据实际错误行提出最小修复，说明会创建哪些文件、资源和图层。把脚本生成验证、Painter 内运行验证和保存验证分别记录。
- 出错后先确认执行到了哪一步。选层失败时检查现有填充层。保存失败时追溯序列化之前的资源错误。不要把再次运行生成器当作默认修复。
- 让 AI 同时看材质参考、当前视口和日志。反馈可直接使用「白梁侧光下像软包」「Base Color 正常、Height 关掉后鼓包消失」「另存仍提示 Roughness PNG 读取失败」这类可定位描述。
- 仓库里的日志使用通用路径与纹理集显示名。实际恢复时以当前 Painter 日志路径为准。

[Adobe Painter 填充图层与投射 API](https://experienceleague.adobe.com/en/docs/substance-3d-dev/painter-python/api/substancepainter-package/layerstack-module/layers-and-effects/fill)

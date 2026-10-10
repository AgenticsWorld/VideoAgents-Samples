# refs/ — 用户参考目录

把「希望成片长成什么样」的参考图、希望使用的音频和文本资料放进来,相关 Agent 会优先参考/选用(约定见 agents/WORKFLOW.md §2)。
**推荐用 Web 客户端【项目预览 → 参考文件】页上传与管理**:按分类预览、上传文件,并给每个文件添加注释说明用途。

- `style/`      整体视觉风格:画风/渲染质感/色调/构图
- `characters/` 角色形象;按角色建子目录(如 characters/linzhao/)可定向到该角色
- `scenes/`     场景与世界观:建筑/地貌/氛围
- `props/`      道具/法宝;服装放 props/costumes/
- `music/`      希望使用的音频文件(背景音轨,BGM 候选,mp3/wav/flac 等);配乐 Agent 优先选用,并自动判断用在视频的合适位置
- `video/`      参考视频:动作/运镜/节奏/转场范例(mp4/mov/webm),视频生成 Agent 优先参考(支持时经 --ref-video 注入)
- `thumbnail/`  封面参考:他人爆款封面/构图/版式范例
- `fonts/`      字体文件(ttf/otf/ttc):花字、封面、片头片尾、字幕等一切需要字体的工位统一优先使用;
                花字引擎自动并入字体清单,font_id 为 `proj:<family>`
- `text/`       文本资料:设定/文案等(txt/md 等),相关 Agent 参考使用
- `NOTES.md`    逐文件注释:哪个文件管什么、想用在哪(有则 Agent 必读)。
                注释在【参考文件】页逐文件填写,自动写入本文件的标记块(机器可读版在 annotations.json)

规则:用户参考素材 > Agent 自行发挥;与文字设定冲突时 Agent 会上报你裁决;目录为空不影响流程。

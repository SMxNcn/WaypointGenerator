# generate_flower.py
from path_utils import parse_action_keys, action_to_json, save_to_output

def generate_flower_cane(p1, p2, final_end, key_combo, filename):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    xf, yf, zf = final_end

    dx = abs(x2 - x1)
    dz = abs(z2 - z1)

    print(f"🔍 调试信息: P1({x1},{z1}) -> P2({x2},{z2}) -> Final({xf},{zf})")
    print(f"   dx={dx}, dz={dz}")

    # 1. 判定轴向
    if dz < 5 and dx >= 5:
        length_axis = 'x'
        spacing_axis = 'z'
        step_val = z2 - z1
        len_val_odd = x1
        len_val_even = x2
        start_sp = z1
        end_sp_target = zf
    elif dx < 5 and dz >= 5:
        length_axis = 'z'
        spacing_axis = 'x'
        step_val = x2 - x1
        len_val_odd = z1
        len_val_even = z2
        start_sp = x1
        end_sp_target = xf
    else:
        print(f"❌ 错误: 无法判定行方向 (dx={dx}, dz={dz})")
        return

    if step_val == 0:
        print("❌ 行间距不能为 0")
        return

    # 2. 解析按键
    key_combo = key_combo.upper().strip()

    if ',' in key_combo:
        # 新格式: "WA,WD" -> 奇数行 WA，偶数行 WD
        parts = [p.strip() for p in key_combo.split(',')]
        if len(parts) != 2:
            print("❌ 逗号格式错误，请使用如 WA,WD 的格式")
            return
        key_odd_str, key_even_str = parts
        key_odd = parse_action_keys(key_odd_str, 'flower')
        key_even = parse_action_keys(key_even_str, 'flower')
    else:
        # 旧格式: "SD" -> 两个单字符
        keys = [k for k in key_combo if k in 'WSAD']
        if len(keys) < 2:
            print("❌ 需要输入 2 个方向键 (如 SD)，或使用逗号分隔的多键组合 (如 WA,WD)")
            return
        key_odd = parse_action_keys(keys[0], 'flower')
        key_even = parse_action_keys(keys[1], 'flower')

    # 3. 动态生成规律路径点 (直到覆盖终点范围)
    waypoints = []
    i = 0
    while True:
        current_sp = start_sp + i * step_val
        
        # 判断是否已经到达或超过终点范围
        if step_val > 0:
            if current_sp > end_sp_target + 0.5: break
        else:
            if current_sp < end_sp_target - 0.5: break

        current_len = len_val_odd if (i % 2 == 0) else len_val_even
        
        if length_axis == 'x':
            cx = current_len
            cz = current_sp
        else:
            cx = current_sp
            cz = current_len
            
        cy = y1

        action = key_odd if (i % 2 == 0) else key_even
        
        waypoints.append({
            "id": len(waypoints) + 1,
            "x": int(cx),
            "y": int(cy),
            "z": int(cz),
            "action": action_to_json(action)
        })
        
        i += 1
        if i > 1000:
            print("⚠️ 生成点数过多，已停止")
            break

    # 4. ✅ 核心修正：在规律点之后，直接追加一个终点路点
    # 这个点不参与奇偶交替逻辑，它的唯一任务就是引导玩家走到精准的终点坐标
    if waypoints:
        # 确定最后一个规律点的动作，以便决定终点点的动作（通常保持相同或设为空）
        # 这里我们让终点点也保持左键点击，确保耕完最后一格
        last_action = key_odd if ((i - 1) % 2 == 0) else key_even
        
        waypoints.append({
            "id": len(waypoints) + 1,
            "x": xf,
            "y": yf,
            "z": zf,
            "action": action_to_json(last_action)
        })
        print(f"   ✅ 已追加终点路点: ({xf}, {yf}, {zf})")

    if not waypoints:
        print("❌ 未生成任何路径点")
        return

    print(f"📐 共生成 {len(waypoints)} 个路径点 (含终点)")
    save_to_output(filename, waypoints)

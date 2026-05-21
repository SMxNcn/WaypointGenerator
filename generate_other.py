# generate_other.py
from path_utils import parse_action_keys, action_to_json, save_to_output

def generate_other(p1, p1_end, p2_start, final_end, straight_key_odd, straight_key_even, turn_key, filename):
    x1, y1, z1 = p1
    xe, ye, ze = p1_end
    xs, ys, zs = p2_start
    xf, yf, zf = final_end

    # 1. 计算基础向量
    # 行向量：从起点到第一行终点
    row_dx = xe - x1
    row_dz = ze - z1
    
    # 步进向量：从第一行终点到第二行起点 (包含了转弯+下移)
    step_dx = xs - xe
    step_dz = zs - ze

    print(f"🔍 调试信息:")
    print(f"   行向量: ({row_dx}, {row_dz})")
    print(f"   步进向量: ({step_dx}, {step_dz})")

    if row_dx == 0 and row_dz == 0:
        print("❌ 起点和第一行终点不能重合")
        return

    # 2. 解析按键
    action_straight_odd = parse_action_keys(straight_key_odd, 'other')   # 第1,3,5...行直行
    action_straight_even = parse_action_keys(straight_key_even, 'other') # 第2,4,6...行直行
    action_turn = parse_action_keys(turn_key, 'other')                   # 转弯动作

    # 3. 生成路径点
    waypoints = []
    
    # 初始基准点
    base_x, base_y, base_z = x1, y1, z1
    
    # 循环计数器
    cycle_count = 0
    max_cycles = 1000 # 防止死循环
    
    while cycle_count < max_cycles:
        current_start_x = base_x + cycle_count * (step_dx) # 简化假设：每两行X/Z偏移一个Step? 
        
        group_offset_x = cycle_count * (2 * step_dx)
        group_offset_z = cycle_count * (2 * step_dz)
        
        # 生成组内4个点
        pts_in_group = [
            (0, 0), 
            (row_dx, row_dz), 
            (row_dx + step_dx, row_dz + step_dz), 
            (step_dx, step_dz)
        ]
        
        for i, (ox, oz) in enumerate(pts_in_group):
            cx = x1 + group_offset_x + ox
            cz = z1 + group_offset_z + oz
            
            # 检查是否超出终点边界 (简单判断：如果步进轴超过终点即停止)
            # 确定步进轴
            if abs(step_dz) > abs(step_dx):
                if (step_dz > 0 and cz > zf + 1) or (step_dz < 0 and cz < zf - 1):
                    break
            else:
                if (step_dx > 0 and cx > xf + 1) or (step_dx < 0 and cx < xf - 1):
                    break

            # 分配动作
            # Pt1 (i=0): Odd Straight
            # Pt2 (i=1): Turn
            # Pt3 (i=2): Even Straight
            # Pt4 (i=3): Turn
            if i == 0:
                action = action_straight_odd
            elif i == 1:
                action = action_turn
            elif i == 2:
                action = action_straight_even
            else:
                action = action_turn
                
            waypoints.append({
                "id": len(waypoints) + 1,
                "x": int(cx),
                "y": y1,
                "z": int(cz),
                "action": action_to_json(action)
            })
            
        cycle_count += 1
        
        # 安全检查：如果最后一个点已经非常接近或超过终点，停止
        if waypoints:
            last = waypoints[-1]
            if abs(step_dz) > abs(step_dx):
                 if (step_dz > 0 and last['z'] >= zf) or (step_dz < 0 and last['z'] <= zf):
                     break
            else:
                 if (step_dx > 0 and last['x'] >= xf) or (step_dx < 0 and last['x'] <= xf):
                     break

    # 4. 强制包含终点坐标
    if waypoints:
        last_wp = waypoints[-1]
        last_wp['x'] = xf
        last_wp['y'] = yf
        last_wp['z'] = zf
        print(f"   ✅ 已强制修正最后一点为终点: ({xf}, {yf}, {zf})")

    if not waypoints:
        print("❌ 未生成任何路径点")
        return

    print(f"📐 共生成 {len(waypoints)} 个路径点")
    save_to_output(filename, waypoints)
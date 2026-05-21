import sys
from path_utils import parse_coord
from generate_flower import generate_flower_cane
from generate_other import generate_other

def main():
    print("🌾 SkyBlock Garden Path Generator")
    print("=" * 40)
    
    # 1. 选择模式
    print("\n选择模式:")
    print("  1. Flower/Cane (2 键交替 / 锯齿状)")
    print("  2. Other (4 点循环 / 标准 S 形)")
    mode = input("请输入模式编号 (1/2): ").strip()
    
    if mode not in ['1', '2']:
        print("❌ 无效的模式选择")
        return
    
    # 2. 公共参数
    filename = input("输出文件名 (如 farm_path.json): ").strip()
    if not filename:
        filename = "path.json"
    else:
        # 如果没有 .json 后缀，自动添加
        if not filename.endswith('.json'):
            filename += '.json'
        
    try:
        p1_str = input("第一行起点坐标 (x,y,z): ").strip()
        p1 = parse_coord(p1_str)
        
        final_end_str = input("路径终点坐标 (x,y,z): ").strip()
        final_end = parse_coord(final_end_str)
    except ValueError as e:
        print(e)
        return

    if mode == '1':
        # === Flower/Cane 模式 ===
        try:
            p2_str = input("第二行起点坐标 (x,y,z): ").strip()
            p2 = parse_coord(p2_str)
        except ValueError as e:
            print(e)
            return
            
        key_combo = input("交替按键组合 (如 SD 或 SA): ").strip()
        if not key_combo:
            print("❌ 按键组合不能为空")
            return
            
        generate_flower_cane(p1, p2, final_end, key_combo, filename)
        
    else:
        # === Other 模式 ===
        try:
            p1_end_str = input("第一行终点坐标 (x,y,z): ").strip()
            p1_end = parse_coord(p1_end_str)
            
            p2_start_str = input("第二行起点坐标 (x,y,z): ").strip()
            p2_start = parse_coord(p2_start_str)
        except ValueError as e:
            print(e)
            return
            
        straight_key_odd = input("正向直行按键 (第1/3/5行, 如 WL): ").strip()
        straight_key_even = input("反向直行按键 (第2/4/6行, 如 AL): ").strip()
        turn_key = input("转弯按键 (如 D): ").strip()
        
        generate_other(p1, p1_end, p2_start, final_end, straight_key_odd, straight_key_even, turn_key, filename)

if __name__ == "__main__":
    main()
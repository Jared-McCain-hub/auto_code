def detect_bridge_type():
    X0_BRIDGE, Y0_BRIDGE = 18, 15
    W_BRIDGE, H_BRIDGE = 280 - X0_BRIDGE, 284 - Y0_BRIDGE

    BRIDGE_KEYWORD = '连接杆'
    img = np.array(pyautogui.screenshot(region=(X0_BRIDGE, Y0_BRIDGE, W_BRIDGE, H_BRIDGE)))
    results = reader.readtext(img)
    texts = [text for _, text, _ in results]
    if any(BRIDGE_KEYWORD in t for t in texts):
        print("检测到 '连接杆'，判定为牙桥（Bridge）。")
        return 'bridge'
    else:
        print("未检测到 '连接杆'，判定为单冠（Single Crown）。")
        return 'single'
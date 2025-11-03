#!/usr/bin/env python3
"""
測試完整的交易流程，根據教學中的示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fubon_mcp.server import (
    place_order, get_order_results, modify_price,
    get_account_info, get_inventory, get_bank_balance,
    get_filled_reports, get_order_reports, get_order_changed_reports
)

def test_trading_workflow():
    """測試完整的交易工作流程"""

    print("=== 測試完整的交易工作流程 ===\n")

    # 1. 檢查帳戶資訊
    print("1. 檢查帳戶資訊...")
    account_info = get_account_info({"account": ""})  # 獲取所有帳戶
    if account_info['status'] == 'success':
        accounts = account_info['data']
        if accounts:
            account_number = accounts[0]['account']
            print(f"找到帳戶: {account_number}")
        else:
            print("未找到任何帳戶")
            return
    else:
        print(f"獲取帳戶資訊失敗: {account_info['message']}")
        return

    # 2. 檢查銀行餘額
    print("\n2. 檢查銀行餘額...")
    balance = get_bank_balance({"account": account_number})
    if balance['status'] == 'success':
        print(f"銀行餘額: {balance['data']}")
    else:
        print(f"獲取銀行餘額失敗: {balance['message']}")

    # 3. 檢查庫存
    print("\n3. 檢查庫存...")
    inventory = get_inventory({"account": account_number})
    if inventory['status'] == 'success':
        print(f"庫存資訊: {inventory['data']}")
    else:
        print(f"獲取庫存失敗: {inventory['message']}")

    # 4. 模擬買入股票 (使用教學中的示例參數)
    print("\n4. 模擬買入富邦金 (2881)...")
    buy_order = {
        "account": account_number,
        "symbol": "2881",
        "quantity": 1000,  # 1張 = 1000股
        "price": 66.0,
        "buy_sell": "Buy",
        "market_type": "Common",
        "price_type": "Limit",
        "time_in_force": "ROD",
        "order_type": "Stock",
        "user_def": "From_Test",
        "is_non_blocking": False
    }

    buy_result = place_order(buy_order)
    if buy_result['status'] == 'success':
        print(f"買入委託成功: {buy_result['message']}")
    else:
        print(f"買入委託失敗: {buy_result['message']}")
        return

    # 5. 檢查委託結果
    print("\n5. 檢查委託結果...")
    order_results = get_order_results({"account": account_number})
    if order_results['status'] == 'success':
        orders = order_results['data']
        if orders:
            print(f"找到 {len(orders)} 筆委託")
            for i, order in enumerate(orders[:3]):  # 只顯示前3筆
                # OrderResult 對象的屬性
                symbol = getattr(order, 'stock_no', 'N/A')
                buy_sell = getattr(order, 'buy_sell', 'N/A')
                quantity = getattr(order, 'quantity', 'N/A')
                price = getattr(order, 'price', 'N/A')
                order_no = getattr(order, 'order_no', 'N/A')
                status = getattr(order, 'status', 'N/A')
                print(f"委託 {i+1}: {symbol} {buy_sell} {quantity}股 @ {price}元 (單號: {order_no}, 狀態: {status})")
        else:
            print("沒有找到委託記錄")
    else:
        print(f"獲取委託結果失敗: {order_results['message']}")

    # 6. 模擬修改委託價格 (如果有委託存在的話)
    if order_results['status'] == 'success' and order_results['data']:
        print("\n6. 模擬修改委託價格...")
        first_order = order_results['data'][0]
        order_no = getattr(first_order, 'order_no', None)
        if order_no:
            modify_result = modify_price({
                "account": account_number,
                "order_no": order_no,
                "new_price": 66.5
            })
            if modify_result['status'] == 'success':
                print(f"修改價格成功: {modify_result['message']}")
            else:
                print(f"修改價格失敗: {modify_result['message']}")
        else:
            print("無法獲取委託單號，跳過修改價格測試 (可能是因為盤後時段)")
    else:
        print("\n6. 跳過修改委託價格測試 (沒有委託記錄)")
    # 8. 檢查成交回報
    print("\n8. 檢查成交回報...")
    filled_reports = get_filled_reports({"limit": 5})
    if filled_reports['status'] == 'success':
        reports = filled_reports['data']
        if reports:
            print(f"找到 {len(reports)} 筆成交回報")
            for i, report in enumerate(reports[:3]):  # 只顯示前3筆
                content = report.get('content', {})
                if hasattr(content, 'filled_qty') and content.filled_qty:
                    print(f"成交 {i+1}: {getattr(content, 'stock_no', 'N/A')} {getattr(content, 'buy_sell', 'N/A')} {content.filled_qty}股 @ {content.filled_price}元 (單號: {getattr(content, 'order_no', 'N/A')})")
                else:
                    print(f"成交 {i+1}: {report}")
        else:
            print("沒有找到成交回報記錄 (可能是因為沒有實際成交)")
    else:
        print(f"獲取成交回報失敗: {filled_reports['message']}")

    # 9. 檢查委託回報
    print("\n9. 檢查委託回報...")
    order_reports = get_order_reports({"limit": 5})
    if order_reports['status'] == 'success':
        reports = order_reports['data']
        if reports:
            print(f"找到 {len(reports)} 筆委託回報")
            for i, report in enumerate(reports[:2]):  # 只顯示前2筆
                print(f"委託回報 {i+1}: {report.get('type', 'N/A')} - {report.get('code', 'N/A')}")
        else:
            print("沒有找到委託回報記錄")
    else:
        print(f"獲取委託回報失敗: {order_reports['message']}")

    # 10. 檢查改價/改量/刪單回報
    print("\n10. 檢查改價/改量/刪單回報...")
    changed_reports = get_order_changed_reports({"limit": 5})
    if changed_reports['status'] == 'success':
        reports = changed_reports['data']
        if reports:
            print(f"找到 {len(reports)} 筆改價/改量/刪單回報")
            for i, report in enumerate(reports[:2]):  # 只顯示前2筆
                print(f"改單回報 {i+1}: {report.get('type', 'N/A')} - {report.get('code', 'N/A')}")
        else:
            print("沒有找到改價/改量/刪單回報記錄")
    else:
        print(f"獲取改價/改量/刪單回報失敗: {changed_reports['message']}")

    print("\n=== 測試完成 ===")
    print("注意：成交回報只有在實際有成交時才會有數據。")
    print("委託回報和改單回報會在有相應操作時產生。")

if __name__ == "__main__":
    test_trading_workflow()
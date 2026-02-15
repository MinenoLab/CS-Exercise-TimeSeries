import os
import requests

# ==========================================
# Configuration
# ==========================================
# サーバーのIPアドレス (環境に合わせて変更してください)
API_URL         = "http://172.16.15.XXX:5000/evaluate"
SUBMISSION_FILE = "submission.csv"
USER_ID         = "your_user_id"

def submit_for_evaluation():
    """
    提出ファイルを評価サーバーに送信し、最新の評価指標を表示します。
    """
    # 1. File Existence Check
    if not os.path.exists(SUBMISSION_FILE):
        print(f"❌ エラー: 提出するファイルが見つかりません: {SUBMISSION_FILE}")
        return

    try:
        # 2. Send Request
        print(f"📡 サーバー({API_URL})にデータを送信中...")
        
        with open(SUBMISSION_FILE, 'rb') as f:
            files_to_send = {'file': (SUBMISSION_FILE, f, 'text/csv')}
            data_to_send  = {'user_id': USER_ID}
            
            # Timeout set to 10 seconds
            response = requests.post(API_URL, files=files_to_send, data=data_to_send, timeout=10)

        # 3. Parse Response
        try:
            json_response = response.json()
        except requests.exceptions.JSONDecodeError:
            json_response = None

        print("="*40)

        # 4. Display Results
        if response.status_code == 200 and json_response:
            print("✅ 評価結果 (Success)")
            print("-" * 40)
            
            metrics  = json_response.get('metrics', {})
            meta     = json_response.get('meta', {})
            seg_info = meta.get('segment_info', {})

            # Helper function for formatting
            def format_metric(name, value):
                if value is None:
                    print(f"  {name:<20}: No Data")
                elif isinstance(value, (int, float)):
                    print(f"  {name:<20}: {value:,.6f}")
                else:
                    print(f"  {name:<20}: {value}")

            # --- Main Score ---
            print("  [Main Score]")
            format_metric("Weighted MAE", metrics.get('weighted_mae', 'N/A'))
            
            print("-" * 40)
            
            # --- Time Segmented Scores ---
            print("  [Time Segmented MAE]")
            # 昼間 (09:00 - 18:00)
            format_metric("Day (09-18)", metrics.get('mae_day_9_18'))
            # 夜間 (18:00 - 24:00)
            format_metric("Night (18-24)", metrics.get('mae_night_18_24'))
            # 真夜中 (00:00 - 09:00)
            format_metric("Midnight (00-09)", metrics.get('mae_midnight_0_9'))
            
            print("-" * 40)

            # --- Global Details ---
            print("  [Global Details]")
            format_metric("RMSLE", metrics.get('rmsle', 'N/A'))
            format_metric("MAE (Global)", metrics.get('mae_global', 'N/A'))
            format_metric("RMSE", metrics.get('rmse', 'N/A'))
            format_metric("R2 Score", metrics.get('r2', 'N/A'))
            
            print("-" * 40)
            print(f"  評価行数             : {meta.get('rows_evaluated', 'N/A')} 行")
            if seg_info:
                print(f"   - Day Rows          : {seg_info.get('day_count', 0)}")
                print(f"   - Night Rows        : {seg_info.get('night_count', 0)}")
                print(f"   - Midnight Rows     : {seg_info.get('midnight_count', 0)}")
            print(f"  User ID              : {meta.get('user_id', USER_ID)}")

        # 5. Handle Errors
        elif response.status_code == 429:
             print("⚠️ レート制限 (Rate Limit Exceeded)")
             print("-" * 40)
             print("  1日の制限回数を超えました。明日再試行してください。")

        else:
            print(f"❌ エラー (Status Code: {response.status_code})")
            print("-" * 40)

            if json_response and 'error' in json_response:
                print(f"  エラーメッセージ: {json_response['error']}")
            elif response.text:
                print(f"  サーバーからの応答:\n{response.text}")
            else:
                print("  サーバーから詳細なエラーメッセージを取得できませんでした。")

        print("="*40)

    except requests.exceptions.ConnectionError:
        print("="*40)
        print(f"❌ エラー: サーバーに接続できません。")
        print(f"'{API_URL}' が起動しているか、ネットワーク接続を確認してください。")
        print("="*40)
    except requests.exceptions.Timeout:
        print("="*40)
        print("❌ エラー: リクエストがタイムアウトしました。サーバーが応答していません。")
        print("="*40)
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    submit_for_evaluation()
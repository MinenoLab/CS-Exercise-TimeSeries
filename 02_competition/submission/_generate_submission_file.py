import pandas as pd

START_DATETIME  = 'YYYY-MM-DD 00:00:00'
END_DATETIME    = 'YYYY-MM-DD 23:00:00'
OUTPUT_FILENAME = 'submission.csv'

def generate_submission_file():
    try:
        timestamps = pd.date_range(start=START_DATETIME, end=END_DATETIME, freq='h')
        df = pd.DataFrame({'Timestamp': timestamps, 'Students': 0})

        print("--- 生成データプレビュー ---")
        print(df.head())
        print("----------------------------")

        df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8')
        
        print(f"CSVファイル '{OUTPUT_FILENAME}' が正常に生成されました。")
        print(f"期間: {START_DATETIME} から {END_DATETIME} まで")
        print(f"総行数: {len(df)}")

    except Exception as e: print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    generate_submission_file()
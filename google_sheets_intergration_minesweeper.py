import requests
import threading

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz49EMwvqYLW9aOgymCrsnMT4yxon9m9gydaq2V2w2tE1_cf9TmZHHjMqG56RlWqXI2/exec"

def do_submit_score(name: str, time: str, difficulty: str) -> None:
    data = {
        "name": name,
        "time": time,
        "difficulty": difficulty
    }
    response = requests.post(WEB_APP_URL, json=data)
    if response.ok:
        print("Score submitted:", response.json())
    else:
        print("Error submitting score:", response.text)

def submit_score(name: str, time: str, difficulty: str):
    def run():
        try:
            data = {
                "name": name,
                "time": time,
                "difficulty": difficulty
            }
            response = requests.post(WEB_APP_URL, json=data, timeout=10)
            result = response.json()
            print("Score submitted:", result)

            # Show a message on the main thread
        except Exception as e:
            print("Error:", e)

    threading.Thread(target=run).start()

def get_leaderboard(difficulty: str) -> list:
    params = {"difficulty": difficulty}
    try:
        response = requests.get(WEB_APP_URL, params=params)
        if response.ok:
            scores = response.json()
            if __name__ == "__main__":
                for i, entry in enumerate(scores, 1):
                    print(entry)
                    print(f"{i}. {entry['name']} - Time: {entry['time']:.3f} - Date: {entry['date'][0:10]}")
            return scores
        else:
            print("Failed to fetch scores:", response.text)
    except requests.exceptions.ConnectionError:
        return False

if __name__ == "__main__":
    #submit_score("Dylan", "32.712540581", "Medium")
    get_leaderboard("Easy")
    
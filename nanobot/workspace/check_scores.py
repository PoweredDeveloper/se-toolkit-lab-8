#!/usr/bin/env python3
import httpx
import json

BASE_URL = "http://127.0.0.1:42001"
API_KEY = "key"

headers = {"Authorization": f"Bearer {API_KEY}"}

# Get all labs
response = httpx.get(f"{BASE_URL}/items/", headers=headers)
items = response.json()
labs = [item for item in items if item.get("type") == "lab"]

print("=" * 60)
print("LMS SCORES SUMMARY")
print("=" * 60)

# Map lab IDs to lab-XX format
lab_mapping = {
    1: "lab-01",
    2: "lab-02", 
    3: "lab-03",
    4: "lab-04",
    5: "lab-05",
    6: "lab-06",
    7: "lab-07",
    8: "lab-08",
}

for lab in labs:
    lab_id = lab["id"]
    lab_title = lab["title"]
    lab_key = lab_mapping.get(lab_id, f"lab-{lab_id:02d}")
    
    print(f"\n{'=' * 60}")
    print(f"{lab_title} ({lab_key})")
    print(f"{'=' * 60}")
    
    # Completion rate
    response = httpx.get(f"{BASE_URL}/analytics/completion-rate", headers=headers, params={"lab": lab_key})
    if response.status_code == 200:
        data = response.json()
        print(f"  Completion: {data['completion_rate']:.1f}% ({data['passed']}/{data['total']} students)")
    
    # Pass rates per task
    response = httpx.get(f"{BASE_URL}/analytics/pass-rates", headers=headers, params={"lab": lab_key})
    if response.status_code == 200:
        data = response.json()
        print(f"  Task Scores (avg):")
        for task in data[:5]:  # Show first 5 tasks
            print(f"    - {task['task']}: {task['avg_score']:.1f}% ({task['attempts']} attempts)")
        if len(data) > 5:
            print(f"    ... and {len(data) - 5} more tasks")
    
    # Group performance
    response = httpx.get(f"{BASE_URL}/analytics/groups", headers=headers, params={"lab": lab_key})
    if response.status_code == 200:
        data = response.json()
        top_groups = sorted(data, key=lambda x: x['avg_score'], reverse=True)[:3]
        print(f"  Top Groups:")
        for group in top_groups:
            print(f"    - {group['group']}: {group['avg_score']:.1f}% avg ({group['students']} students)")
    
    # Top learners
    response = httpx.get(f"{BASE_URL}/analytics/top-learners", headers=headers, params={"lab": lab_key, "limit": 3})
    if response.status_code == 200:
        data = response.json()
        print(f"  Top Learners:")
        for learner in data:
            print(f"    - Learner #{learner['learner_id']}: {learner['avg_score']:.1f}% avg ({learner['attempts']} attempts)")

print(f"\n{'=' * 60}")
print(f"Total Labs: {len(labs)}")
print(f"Total Learners: 258")
print(f"{'=' * 60}")

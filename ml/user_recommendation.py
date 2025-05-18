# backend/ml/user_recommendation.py

from collections import defaultdict

def recommend_events(user_id: int, user_bookings: dict, all_events: list, top_n: int = 5):
    """
    Simple user-based collaborative filtering:
    - user_bookings: dict of user_id -> list of event_ids booked
    - all_events: list of event dicts with event info (id, name, category, etc.)
    Returns a list of recommended event dicts.
    """
    # 1. Get events the user already booked
    user_events = set(user_bookings.get(user_id, []))
    
    # 2. Find users who share events with this user
    similar_users = []
    for other_user, events in user_bookings.items():
        if other_user == user_id:
            continue
        if user_events.intersection(events):
            similar_users.append(other_user)
    
    # 3. Collect events booked by similar users, excluding user's own events
    recommended_event_counts = defaultdict(int)
    for su in similar_users:
        for event_id in user_bookings.get(su, []):
            if event_id not in user_events:
                recommended_event_counts[event_id] += 1
    
    # 4. Sort events by frequency and pick top N
    recommended_event_ids = sorted(recommended_event_counts, key=recommended_event_counts.get, reverse=True)[:top_n]
    
    # 5. Map event_ids to event info
    recommended_events = [event for event in all_events if event['id'] in recommended_event_ids]
    
    return recommended_events

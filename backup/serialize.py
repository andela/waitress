def serialize_meal(payload):
    return dict(
        date=str(payload[0]),
        user_id=payload[2],
        first_name=payload[3],
        last_name=payload[4],
        breakfast=payload[6],
        lunch=payload[7],
    )

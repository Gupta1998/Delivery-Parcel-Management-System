import pandas as pd
from ..models import Parcel

def generate_report():
    parcels = Parcel.query.all()
    data = [{'id': p.id, 'sender': p.sender, 'receiver': p.receiver, 'status': p.status, 'creation date': p.created_at} for p in parcels]
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

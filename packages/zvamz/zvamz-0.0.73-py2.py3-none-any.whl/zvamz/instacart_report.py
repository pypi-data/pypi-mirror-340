import pandas as pd
import numpy as np
from datetime import datetime, timezone

def insta_ads_report(filePath:str):
    instaDf = pd.read_csv(filePath)
    instaDf['date'] = pd.to_datetime(instaDf['date'])

    req_columns = [
        'date',
        'status',
        'campaign',
        'ad_group',
        'product',
        'product_size',
        'upc',
        'spend',
        'attributed_sales',
        'attributed_quantities',
        'roas',
        'impressions',
        'clicks',
        'ctr',
        'average_cpc',
        'ntb_attributed_sales',
        'percent_ntb_attributed_sales',
        'id',
        'campaign_uuid',
        'ad_group_uuid'
    ]

    missingColumns = set(req_columns) - set(instaDf.columns)
    newColumns = set(instaDf.columns) - set(req_columns)

    if missingColumns or newColumns:
        message = (
        f"""
        missing columns: {', '.join(missingColumns)}
        new columns: {', '.join(newColumns)}
        """
        )

        raise ValueError(message)

    instaDf = instaDf[req_columns]

    schema = {
        'date' : 'datetime64[ns]',
        'status' : str,
        'campaign' : str,
        'ad_group' : str,
        'product' : str,
        'product_size' : str,
        'upc' : str,
        'spend' : float,
        'attributed_sales' : float,
        'attributed_quantities' : float,
        'roas' : float,
        'impressions' : float,
        'clicks' : float,
        'ctr' : float,
        'average_cpc' : float,
        'ntb_attributed_sales' : float,
        'percent_ntb_attributed_sales' : float,
        'id' : str,
        'campaign_uuid' : str,
        'ad_group_uuid' : str
    }

    instaDf = instaDf.astype(schema)
    return instaDf


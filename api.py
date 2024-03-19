from crawler import crawl
from cache_mongodb import MongoDB
from pydantic import BaseModel

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded

# Create a limiter instance
limiter = Limiter(key_func=get_remote_address)

# Initialize your FastAPI app
app = FastAPI()

# Register the rate limit exceeded handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply the rate limit to your endpoints


app = FastAPI()


class GetPrices(BaseModel):
    latitude: float | None
    longitude: float | None


m = MongoDB("api_cache_data")


@app.post("/prices")
@limiter.limit("1440/minute")
def get_prices(prices: GetPrices, request: Request):
    res = m.search_one(
        {'coordinates': [prices.latitude, prices.longitude]})
    if res is not None:
        res.pop('_id', None)
        return res

    else:
        # print(await crawl(lat=prices.latitude, lon=prices.longitude))
        data = crawl(lat=prices.latitude, lon=prices.longitude)

        if data is not None:
            changed_data = {
                'coordinates': [prices.latitude, prices.longitude],
                'data': data}
            m.post(changed_data)
            changed_data.pop('_id', None)
            return changed_data
        return {f"{prices.latitude} {prices.longitude}": "Data not available"}

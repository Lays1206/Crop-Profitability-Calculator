# Stardew Valley Crop Profitability Calculator (WIP) 

A Django REST Framework API that models Stardew Valley crops, seasons, and fertilizers to help players find the most profitable crops for each season. A React frontend is in progress.

*Unofficial fan project; Stardew Valley is created by ConcernedApe.
All game information was found on the Stardew Valley Wiki.*

**Tech Stack:** Python, Django, Django REST Framework, React (planned)

## Status
- Models (Crops, Seasons, Fertilizer, Fertilizer Quality), serializers, and views
  implemented
- Management commands populate crop, season, and fertilizer data from CSVs

## API Routes
- `GET /api/`: API root containing all possible routes
- `GET /api/crops/`: returns entire list of crops containing name, growing seasons, a special
  location (default of None), growth time (days to maturity), sell price, seed price,
  multiharvest (boolean), days to regrow (if multiharvest), and max harvests (default of 1)
- `GET /api/crops/<int:pk>/`: returns a detail list of a specific crop given crop's id
- `GET /api/seasons/`: returns entire list of seasons
- `GET /api/quality-chance/`: returns entire list of fertilizer type and farming level combinations,
  along with the percentage chance for each quality level and the average price multiplier for crop
  sell price
- `GET /api/gold-per-day/`: returns a list of crops ordered by guaranteed minimum gold-per-day, descending

## Query Parameters

| Param | Used by | Accepted values | Default |
|---|---|---|---|
| `season` | `/api/crops/` | Spring, Summer, Fall, Winter | all seasons |
| `farming_level` | `/api/gold-per-day/` | 0-14 | 0 |
| `fertilizer` | `/api/gold-per-day/` | Basic, Quality, Deluxe | None |

Invalid values return a 400 error.

## Example

```
GET /api/gold-per-day/?farming_level=1&fertilizer=Deluxe
```

Response (trimmed):
```json
[
    {
        "id": 47,
        "name": "Sweet Gem Berry",
        "sell_price": 3000,
        "seed_price": 1000,
        "gold_per_day": 128.33
    },
    {
        "id": 23,
        "name": "Starfruit",
        "sell_price": 750,
        "seed_price": 400,
        "gold_per_day": 47.69
    },
    {
        "id": 44,
        "name": "Pineapple",
        "sell_price": 300,
        "seed_price": 0,
        "gold_per_day": 43.71
    },
    ...
    {
        "id": 4,
        "name": "Coffee Bean",
        "sell_price": 15,
        "seed_price": 2500,
        "gold_per_day": -82.0
    }
]
```

In the above example, `gold_per_day` accounts for seed price and the average price multiplier for the given farming level and fertilizer type (Basic, Quality, Deluxe). Negative values mean a crop loses gold-per-day. A seed price of 0 means seeds aren't sold in shops, so no seed cost is deducted.

## Setup
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py load_crop_data`
4. `python manage.py load_fertilizer_data`
5. `python manage.py runserver`

## Roadmap
- User accounts and saved farm plans (POST endpoint)
- React frontend for browsing and comparing crops

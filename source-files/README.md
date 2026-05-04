# Source Files

Place the following CSV files in this folder before running the pipeline:

| File | Description | Key Columns |
|------|-------------|-------------|
| `bookings.csv` | Flight booking transactions | `booking_id`, `passenger_id`, `flight_id`, `airport_id`, `amount`, `booking_date` |
| `passengers.csv` | Passenger profiles | `passenger_id`, `name`, `gender`, `nationality` |
| `airports.csv` | Airport reference data | `airport_id`, `airport_name`, `city`, `country` |

## Notes

- `booking_date` should be in `YYYY-MM-DD` format
- `passenger_id` is the join key between `bookings` and `passengers`
- `airport_id` is the join key between `bookings` and `airports`

## Sample Data

Sample data was generated using the [Faker](https://faker.readthedocs.io/) library.
You can generate your own using tools like [Mockaroo](https://mockaroo.com/) or ask Claude to generate synthetic data.

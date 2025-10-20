# modules/generator.py

import uuid
import random
import faker
import datetime

fake = faker.Faker()

def generate_value(field_spec):
    """Generate a value based on the schema specification."""
    ftype = field_spec.get("type")

    if ftype == "string":
        gen = field_spec.get("generator", "")
        if gen == "uuid":
            return str(uuid.uuid4())
        elif gen == "faker.company":
            return fake.company()
        elif "values" in field_spec:
            return random.choice(field_spec["values"])
        else:
            return fake.word()

    elif ftype == "float":
        return round(random.uniform(field_spec.get("min", 0), field_spec.get("max", 1)), 2)

    elif ftype == "int":
        return random.randint(field_spec.get("min", 0), field_spec.get("max", 100))

    elif ftype == "date":
        start, end = field_spec.get("range", ["2018-01-01", "2022-01-01"])
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return (start_date + datetime.timedelta(days=random_days)).strftime("%Y-%m-%d")

    elif ftype == "bool":
        return random.choice([True, False])

    else:
        return None


def generate_records(schema, num_records=100, seed=42):
    """Generate synthetic records based on schema."""
    random.seed(seed)
    faker.Faker.seed(seed)

    records = []

    for _ in range(num_records):
        record = {}
        for field, spec in schema.items():
            if "calculated" in spec:
                # Placeholder, will be filled by business rules
                record[field] = 0
            else:
                record[field] = generate_value(spec)
        records.append(record)

    return records

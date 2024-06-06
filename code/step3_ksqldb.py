import requests
import json

KSQLDB_SERVER = "http://localhost:8088"

INPUT_TOPIC = "step2-sa"
OUTPUT_TOPIC = "step3-agg"

def execute_ksql_query(ksql_string):
    headers = {
        'Content-Type': 'application/vnd.ksql.v1+json; charset=utf-8',
        'Accept': 'application/vnd.ksql.v1+json'
    }
    payload = {
        'ksql': ksql_string,
        'streamsProperties': {}
    }
    response = requests.post(f"{KSQLDB_SERVER}/ksql", headers=headers, data=json.dumps(payload))
    return response.json()

def create_streams_and_tables():
    # Define queries
    create_streams_query = f"""
    CREATE STREAM MALETAS_STREAM (
        id INTEGER,
        text VARCHAR,
        country VARCHAR,
        sentiment VARCHAR
    ) WITH (
        KAFKA_TOPIC='{INPUT_TOPIC}',
        VALUE_FORMAT='JSON'
    );

    CREATE TABLE SENTIMENT_AGG AS
    SELECT
        'constant_key' AS dummy_key,
        COUNT(*) AS total_count,
        SUM(CASE WHEN sentiment = 'Positive' THEN 1 ELSE 0 END) AS positive_count,
        SUM(CASE WHEN sentiment = 'Negative' THEN 1 ELSE 0 END) AS negative_count,
        SUM(CASE WHEN sentiment = 'Neutral' THEN 1 ELSE 0 END) AS neutral_count
    FROM MALETAS_STREAM
    GROUP BY 'constant_key'
    EMIT CHANGES;

    CREATE TABLE SENTIMENT_AGG_OUTPUT
    WITH (KAFKA_TOPIC='{OUTPUT_TOPIC}', PARTITIONS=1, REPLICAS=1) AS
    SELECT 
        dummy_key,
        total_count,
        positive_count,
        negative_count,
        neutral_count
    FROM SENTIMENT_AGG
    EMIT CHANGES;
    """

    # Execute queries
    response = execute_ksql_query(create_streams_query)
    print(response)

create_streams_and_tables()


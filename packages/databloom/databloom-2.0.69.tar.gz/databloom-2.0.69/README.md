# DataBloom SDK Client

A Python SDK client for data integration with PostgreSQL, MySQL, Nessie, and S3.

## Quick Start

```bash
# Setup environment
conda create -n data_bloom python=3.9
conda activate data_bloom

# Install
pip install -e ".[dev]"
```

## Configuration

Create `.env` file with your credentials:

## Testing

```bash
# Run all tests
make test
```

## Development

```bash
make format          # Format code
make lint           # Run linter
make doc            # Build docs
```

## License

VNG License
```sh
curl --location 'https://dev-sdk.ird.vng.vn/v1/sources' --header 'Authorization: Bearer 3d26565c-331a-431f-9f16-3dfd0ee2d204'


curl --location 'https://dev-sdk.ird.vng.vn/v1/sources' --header 'Authorization: Bearer 2cffb5e0-b42b-45a7-a965-8963b9f05d9e'


curl --location 'https://dev-sdk.ird.vng.vn/v1/sources/ConnectorPg1' \
--header 'Authorization: ••••••'



curl --location 'https://dev-sdk.ird.vng.vn/v1/sources/PGIRD' \
--header 'Authorization: Bearer 2cffb5e0-b42b-45a7-a965-8963b9f05d9e'

curl --location 'https://dev-sdk.ird.vng.vn/v1/sources/ird_gsheet' \
--header 'Authorization: Bearer 2cffb5e0-b42b-45a7-a965-8963b9f05d9e'
```


```python

ctx.connector(source="postgresql/ird_gsheet", tablename="")



# TODO run in mysql
engine_mysql = create_sqlalchemy_engine(source="mysql/MYSQLIRD", database="mktvng")
df = pd.read_sql_table("actual_raw_data", con=engine_mysql)
print(df.head())

sql_stmt = """SELECT id, name, value FROM test.test_table_mysql;"""
df = pd.read_sql(sql_stmt, con=engine_mysql)
print(df.head())

```
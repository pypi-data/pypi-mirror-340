supported_formats = {
  'csv':'data',
  'json': 'data',
  'parquet': 'data',
  'pkl': 'data',
  'xlsx': 'data',
  'pdf': 'metadata',
  'png': 'metadata',
  'jpg': 'metadata',
  'jpeg': 'metadata',
}

# these could later be a config file in a user's home directory
default_sample_output_limit = 5
sample_data_table_type = 'simple'
metadata_table_type = 'rounded_grid'
groupby_counts_table_type = 'rounded_grid'
default_max_terminal_width = 80
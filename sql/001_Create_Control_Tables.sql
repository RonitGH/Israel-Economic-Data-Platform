CREATE TABLE IF NOT EXISTS
  `control.source_systems`
(
  source_id STRING NOT NULL,
  source_name STRING NOT NULL,
  source_type STRING NOT NULL,
  source_url STRING,
  landing_path STRING NOT NULL,
  raw_table STRING NOT NULL,
  load_type STRING NOT NULL,
  is_active BOOL NOT NULL,
  last_successful_load TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

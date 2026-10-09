-- Apply once to an existing Tooly database before starting the updated backend.
-- For SQLite; use your database migration system for PostgreSQL / SQL Server.
ALTER TABLE equipment ADD COLUMN trade VARCHAR(12);
CREATE INDEX ix_equipment_trade ON equipment (trade);

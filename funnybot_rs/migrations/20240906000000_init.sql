-- Add migration script here
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE jokes (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	text VARCHAR(1024) NOT NULL UNIQUE,
	type VARCHAR(20) NOT NULL
);

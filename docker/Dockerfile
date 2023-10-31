# Use the official PostgreSQL image from Docker Hub
FROM postgres:13

# Set environment variables (if any)
ENV POSTGRES_USER materials
ENV POSTGRES_PASSWORD materials
ENV POSTGRES_DB materialsDB

# Copy initialization scripts (if any)
# For example, you could add a SQL script to populate the database
COPY ./init.sql /docker-entrypoint-initdb.d/

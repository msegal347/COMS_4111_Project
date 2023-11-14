# Use the official PostgreSQL image from Docker Hub
FROM postgres:15

# Set environment variables (if any)
ENV POSTGRES_USER materials
ENV POSTGRES_PASSWORD materials
ENV POSTGRES_DB materialsDB

# Create a custom script to create the database with the right collation
# Note: Replace `your_collation` with the correct collation for your use case.
RUN echo "CREATE DATABASE materialsDB WITH ENCODING='UTF8' LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' TEMPLATE=template0;" > /docker-entrypoint-initdb.d/00_create_database.sql

# Copy initialization scripts from the 'sql-scripts' directory to '/docker-entrypoint-initdb.d/' where they will be auto-executed during container startup
# The files are renamed to ensure the desired order
COPY ./sql-scripts/create_tables.sql /docker-entrypoint-initdb.d/01_create_tables.sql
COPY ./sql-scripts/general_categories.sql /docker-entrypoint-initdb.d/02_general_categories.sql
COPY ./sql-scripts/insert_materials.sql /docker-entrypoint-initdb.d/03_insert_materials.sql
COPY ./sql-scripts/company.sql /docker-entrypoint-initdb.d/04_company.sql
COPY ./sql-scripts/environmental_impact.sql /docker-entrypoint-initdb.d/05_environmental_impact.sql
COPY ./sql-scripts/industrial_applications.sql /docker-entrypoint-initdb.d/06_industrial_applications.sql
COPY ./sql-scripts/has_effect_on_environment.sql /docker-entrypoint-initdb.d/07_has_effect_on_environment.sql
COPY ./sql-scripts/has_practical_uses.sql /docker-entrypoint-initdb.d/08_has_practical_uses.sql
COPY ./sql-scripts/sold_by.sql /docker-entrypoint-initdb.d/09_sold_by.sql

# Set permissions for the scripts to ensure they are executable
RUN chmod a+r /docker-entrypoint-initdb.d/*

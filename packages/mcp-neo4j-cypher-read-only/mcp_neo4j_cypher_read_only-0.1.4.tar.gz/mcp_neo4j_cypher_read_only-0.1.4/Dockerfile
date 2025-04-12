FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir hatchling

COPY pyproject.toml /app/
COPY README.md /app/

# Install dependencies including boto3
# This will pick up dependencies from pyproject.toml
# Ensure boto3 is listed there
RUN pip install --no-cache-dir neo4j>=5.26.0 mcp>=1.6.0 boto3>=1.28.0

# Copy the source code
COPY src/ /app/src/

# Add src directory to PYTHONPATH to help with module resolution for src layout
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Re-install in editable mode might not be necessary if already installed above
# Consider if just installing '.' is sufficient
# RUN pip install --no-cache-dir -e .

# Environment variables for Neo4j connection
# Password is no longer set here; it will be fetched or passed via args
# Database name can be set here or via CMD args
ENV NEO4J_URL="bolt://host.docker.internal:7687"
ENV NEO4J_USERNAME="neo4j"
# Remove the insecure password ENV
# ENV NEO4J_PASSWORD="password"

# AWS Credentials - provide these during `docker run` using -e for security
# Default region can be useful for boto3
ARG AWS_DEFAULT_REGION=us-west-2
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
# Access Key ID
ARG AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
# Secret Access Key
ARG AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
# Session Token (optional, for temporary credentials)
ARG AWS_SESSION_TOKEN=
ENV AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

# Ensure the script installation directory is in the PATH
ENV PATH="/usr/local/bin:${PATH}"

# Updated command to run the server using the package entry point
# Expects connection details, including secret name/region if used, via command line args
# Example usage (secrets manager): CMD ["mcp-neo4j-cypher-read-only", "--db-url", "${NEO4J_URL}", "--username", "${NEO4J_USERNAME}", "--database", "${NEO4J_DATABASE}", "--secret-name", "your-secret-name", "--secret-region", "${AWS_DEFAULT_REGION}"]
# Example usage (direct password): CMD ["mcp-neo4j-cypher-read-only", "--db-url", "${NEO4J_URL}", "--username", "${NEO4J_USERNAME}", "--database", "${NEO4J_DATABASE}", "--password", "your-actual-password"]

# Make the CMD flexible - it's better to provide the full command during `docker run`
# This entrypoint allows overriding the command easily.
ENTRYPOINT ["sh", "-c"]

# Default command if none is provided to `docker run` (using secrets manager)
# Replace placeholders before building or override at runtime
CMD ["mcp-neo4j-cypher-read-only --db-url $NEO4J_URL --username $NEO4J_USERNAME --secret-name YOUR_SECRET_NAME_HERE --secret-region $AWS_DEFAULT_REGION --log-level INFO"]

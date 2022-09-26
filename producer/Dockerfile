# Base off the official python image
# Define a common stage for dev and prod images called base
FROM python:3.8 as base
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create a user to avoid running containers as root in production
RUN addgroup --system appuser \
    && adduser --system --ingroup appuser appuser
# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
  # dependencies for building Python packages
  build-essential \
  # cleaning up unused files to reduce the image size
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# Switch to the non-root user
USER appuser
# Create a directory for the source code and use it as base path
WORKDIR /home/appuser/code/
# Copy the python depencencies list for pip
COPY --chown=appuser:appuser ./producer/requirements.txt requirements.txt
# Switch to the root user temporary, to grant execution permissions.
USER root
# Install python packages at system level
RUN pip install --no-cache-dir -r requirements.txt
USER appuser


# Define an image for local development. Inherits common packages from the base stage.
FROM base as dev
# The development server starts by default when the container starts
CMD ["python", "main.py"]

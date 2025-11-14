# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MkDocs configuration and source files
COPY mkdocs.yml .
COPY docs/ ./docs/

# Build the site
RUN mkdocs build --site-dir /app/site

# Production stage with nginx
FROM nginx:alpine

# Copy built site from builder
COPY --from=builder /app/site /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]


FROM nginx:alpine-slim

# Copy the self-contained HackRange and CEH v13 cyber training platform assets
COPY index.html /usr/share/nginx/html/index.html
COPY ceh.html /usr/share/nginx/html/ceh.html
COPY ceh_data /usr/share/nginx/html/ceh_data

# Expose HTTP port
EXPOSE 80

# Lightweight container health check
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

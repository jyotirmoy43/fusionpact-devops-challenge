
# Use Nginx to serve static HTML
FROM nginx:alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy your static HTML file into Nginx web root
COPY Devops_Intern.html /usr/share/nginx/html/index.html

# Expose port 80 for web access
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]


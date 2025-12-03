FROM node:18

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Expose port
EXPOSE 5173

# Default command with hot-reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


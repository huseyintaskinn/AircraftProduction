FROM node:20-slim

WORKDIR /app

# Install package dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev port
EXPOSE 5173

# Start Vite dev server with host exposure
CMD ["npm", "run", "dev", "--", "--host"]

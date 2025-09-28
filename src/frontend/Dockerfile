# Stage 1: Builder - Install dependencies and build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install all dependencies including devDependencies (needed for TypeScript)
RUN npm install --include=dev

# Copy all source files
COPY . .

# Build the application
RUN npm run build

# Stage 2: Development - For hot-reloading
FROM node:20-alpine AS development

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies for development)
RUN npm install --include=dev

# Copy built artifacts from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./next.config.ts

# Copy source files for development (enables hot-reloading)
COPY . .

# Environment variables
ENV NODE_ENV=development
ENV NEXT_TELEMETRY_DISABLED=1
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 3000
CMD ["npm", "run", "dev"]

#  or Stage 3: Production - For serving the built application
# FROM node:20-alpine AS production

# WORKDIR /app

# COPY --from=builder /app/package.json .
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/next.config.ts ./next.config.ts  # Changed to .ts
# COPY --from=builder /app/node_modules ./node_modules

# ENV NODE_ENV=production

# EXPOSE 3000
# CMD ["npm", "start"]
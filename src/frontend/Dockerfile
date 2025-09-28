# Stage 1: Builder - Install dependencies and build
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Clear any existing cache and install dependencies
RUN npm cache clean --force
RUN npm install --include=dev

# Copy all source files
COPY . .

# Build the application
RUN npm run build

#  Development - For hot-reloading
FROM node:20-alpine AS development

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies for development)
RUN npm cache clean --force
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

# Production - For serving the built application
FROM --platform=linux/amd64 node:20-alpine AS production

WORKDIR /app

# Create a non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy package.json for production dependencies
COPY --from=builder /app/package.json .
COPY --from=builder /app/package-lock.json .

# Install only production dependencies
RUN npm ci --omit=dev --cache /tmp/.npm

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.ts ./next.config.ts

# Switch to non-root user
USER nextjs

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

EXPOSE 3000
CMD ["npm", "start"]
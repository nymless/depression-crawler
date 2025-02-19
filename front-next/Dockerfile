# Docker multi-stage image building
FROM node:23-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
# Create a standalone build with automatically copying traced files
RUN npm run build

# The .env file is needed only for the build stage
# Make sure .env is not included in the final container
RUN rm -f /app/.next/standalone/.env

# Final build stage
FROM node:23-alpine

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# server.js is created by `next build` in the standalone output
CMD ["node", "server.js"]

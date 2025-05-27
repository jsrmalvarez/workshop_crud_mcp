FROM node:22-alpine

WORKDIR /app

# First copy only package files
COPY package*.json ./

# Clean install
RUN rm -rf node_modules && \
    npm cache clean --force && \
    npm install --no-package-lock

# Then copy the rest
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
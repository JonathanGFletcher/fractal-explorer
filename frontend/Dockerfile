FROM node:lts-alpine AS build

WORKDIR /app/frontend
COPY . .

RUN npm ci

EXPOSE 80
CMD [ "npm", "run", "dev" ]
FROM node:lts-alpine AS build

WORKDIR /app/frontend
COPY . .

RUN npm ci
RUN npm run build



FROM nginx:stable-alpine

COPY --from=build /app/frontend/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
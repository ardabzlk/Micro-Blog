# build stage
FROM node:18.15.0-alpine as build-stage
WORKDIR /app
COPY package.json yarn.lock /code/
RUN yarn install
COPY . .
RUN yarn build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# build stage
FROM node:lts-alpine as build-stage
WORKDIR /home/ubuntu/Together/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

EXPOSE 8080
CMD [ "npm", "run", "serve" ]


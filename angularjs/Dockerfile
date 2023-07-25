# build the angular source code into production output 
FROM node:alpine3.17 as build
RUN mkdir -p /app
WORKDIR /app
COPY package.json /app/
RUN npm install
COPY . .
RUN npm run build --prod
# Serve Application using Nginx Server
FROM nginx:alpine
COPY  --from=build /app/dist/angularjs-python /usr/share/nginx/html
EXPOSE 80
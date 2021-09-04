FROM node:lts-alpine

# bind your app to the gateway IP
ENV HOST=0.0.0.0

# make the 'app' folder the current working directory
WORKDIR /app

# install project dependencies
RUN npm install
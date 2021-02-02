FROM node:14-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY . ./
COPY package.json ./
# COPY package-lock.json ./

#RUN npm install --silent
RUN npm install

RUN npm install -g serve

RUN npm rebuild node-sass
RUN npm run build

# RUN npm install react



CMD ["serve", "-s", "build"]

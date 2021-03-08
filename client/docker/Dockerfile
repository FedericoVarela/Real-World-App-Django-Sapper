FROM node:14.15.1-alpine3.11 AS build

WORKDIR /usr/src/app

COPY package.json rollup.config.js yarn.lock ./
RUN npm install
COPY . .

RUN npm run build


FROM node:14.15.1-alpine3.11

COPY rollup.config.js package.json yarn.lock ./

RUN npm install --only=production

COPY --from=build /usr/src/app/__sapper__/build /__sapper__/build
COPY --from=build /usr/src/app/static/ ./static

ENV HOST=0.0.0.0

CMD [ "npm", "run", "start" ]

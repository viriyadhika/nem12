FROM node:22-alpine

WORKDIR /app

COPY ./frontend_meter_readings/package.json /app

RUN npm install

COPY ./frontend_meter_readings /app

RUN npm run build

EXPOSE 8080

CMD [ "npm", "run", "preview"]
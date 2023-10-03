FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli@5.0.8 -g

COPY package.json .
COPY package-lock.json .
RUN npm install
# vue-cli-service без fix не заводится у меня(
RUN npm audit fix 
RUN npm install bootstrap axios 

CMD ["npm", "run", "serve"]  
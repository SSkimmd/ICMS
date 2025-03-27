FROM node
WORKDIR /store-app
COPY . .
RUN rm .env
RUN cp .env.docker .env
RUN rm .env.docker
RUN npm install --legacy-peer-deps
CMD ["npm", "run", "host"]
FROM node
WORKDIR /icms-app
COPY . .
RUN rm .env.base
RUN cp .env.docker .env
RUN rm .env.docker
RUN npm install
CMD ["npm", "run", "host"]
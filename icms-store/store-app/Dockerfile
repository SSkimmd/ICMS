FROM node
WORKDIR /store-app
COPY . .
RUN rm .env
RUN cp .env.docker .env
RUN rm .env.docker
RUN npm install --legacy-peer-deps
RUN npm run build
CMD ["npm", "run", "preview", "--", "--host"]
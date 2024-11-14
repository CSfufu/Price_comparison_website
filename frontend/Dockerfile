FROM node:18-alpine

WORKDIR /app

COPY price_comparison_website/package*.json /app/

RUN npm install

COPY price_comparison_website /app/

EXPOSE 5173

CMD ["npm", "run", "dev"]

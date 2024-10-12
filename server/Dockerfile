FROM gocv/opencv

WORKDIR /app
RUN mkdir glacier
RUN go install github.com/air-verse/air@latest
COPY . server

WORKDIR /app/server
RUN go mod download

EXPOSE 80
CMD [ "air" ]
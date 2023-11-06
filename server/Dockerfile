FROM golang:1.19

WORKDIR /app
RUN mkdir glacier
RUN go install github.com/cosmtrek/air@latest
COPY . server

WORKDIR /app/server
RUN go mod download

EXPOSE 80
CMD [ "air" ]
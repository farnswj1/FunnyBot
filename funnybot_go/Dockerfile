FROM golang:1.23.0-alpine AS build

WORKDIR /opt/app

COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . ./
RUN go build -o build

FROM alpine

WORKDIR /opt/app

COPY --from=build /opt/app/build ./
COPY --from=build /opt/app/data ./data/

ENTRYPOINT ["./build"]

FROM rust:1.86.0 AS build

WORKDIR /opt/app

# build and cache the dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo fetch
RUN cargo build --release
RUN rm src/main.rs ./target/release/deps/funnybot*

# copy the source code and build for release
COPY . ./
RUN cargo build --release

# the final base image
FROM gcr.io/distroless/cc

WORKDIR /opt/app

# copy the build artifact from the build stage
COPY --from=build /opt/app/target/release/funnybot ./
COPY --from=build /opt/app/data ./data/

# run the binary
CMD ["./funnybot"]

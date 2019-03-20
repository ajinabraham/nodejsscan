FROM python:3-alpine

WORKDIR /usr/src/app

# Copy required files from host to image
COPY ./cli.requirements.txt ./
COPY ./core ./core

# Install required dependencies
RUN pip install --no-cache-dir -r cli.requirements.txt \
    # Move cli.py from /usr/src/app/core to /usr/src/app
    && mv ./core/cli.py .

ENTRYPOINT ["python","/usr/src/app/cli.py"]

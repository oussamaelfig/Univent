FROM python:3.10

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

# Copy source code
COPY . .

# Increase the limit for the number of processes
RUN echo '*               soft    nproc     8192' >> /etc/security/limits.conf
RUN echo '*               hard    nproc     8192' >> /etc/security/limits.conf

# Run the application
CMD ["python", "-m", "unittest", "discover"]

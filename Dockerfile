FROM python:3.12-rc-bookworm


# Add latest version of cairo to sources
# RUN echo "deb http://ftp.us.debian.org/debian buster main" >> /etc/apt/sources.list.d/cairo.list

# # Setup Chrome PPA
# RUN apt-get update && apt-get install -y gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update package list and install chrome, weasyprint and other necessary packages
RUN apt-get update && apt-get install -y wget xvfb unzip google-chrome-stable build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2-dev libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info libpq-dev python3-dev

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
RUN python manage.py collectstatic --noinput
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "-c","gunicorn.conf.py", "invoice_system.wsgi:application"]
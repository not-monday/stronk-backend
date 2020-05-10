# pull official base image
FROM python:3.7

RUN apt-get upgrade
# set work directory
WORKDIR /app
# copy project
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod u+x ./scripts/entrypoint.sh
CMD ["./scripts/entrypoint.sh"]